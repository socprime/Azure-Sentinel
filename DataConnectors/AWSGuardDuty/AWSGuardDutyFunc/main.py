import os
import boto3
from datetime import datetime, timedelta
import logging
import sys
import azure.functions as func

from .sentinel_connector import AzureSentinelConnector


AWS_ACCESS_KEY_ID = os.environ['AWSAccessKeyId']
AWS_SECRET_ACCESS_KEY = os.environ['AWSSecretAccessKey']
AWS_REGION_NAME = os.environ['AWSRegionName']

WORKSPACE_ID = os.environ['AzureSentinelWorkspaceId']
SHARED_KEY = os.environ['AzureSentinelSharedKey']

LOG_TYPE = 'AWSGuardDuty'

PERIOD_MINS = 60 + 1440 * 100  # for testing. function.json also is changed for testing
DELAY_MINS = 5


def main(mytimer: func.TimerRequest):
    mins_from = PERIOD_MINS + DELAY_MINS
    mins_to = DELAY_MINS
    now = datetime.utcnow().replace(second=0, microsecond=0)
    date_from = now - timedelta(minutes=mins_from)
    date_to = now - timedelta(minutes=mins_to)

    logging.info('Script started. Getting findings updated between {} and {}'.format(date_from, date_to))

    ts_ms_from = convert_datetime_to_ts_ms(date_from)
    ts_ms_to = convert_datetime_to_ts_ms(date_to)

    gd_client = GuardDutyConnector(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION_NAME
    )

    sentinel = AzureSentinelConnector(workspace_id=WORKSPACE_ID, shared_key=SHARED_KEY, log_type=LOG_TYPE, queue_size=1000)

    with sentinel:
        for finding in gd_client.get_findings(ts_ms_from=ts_ms_from, ts_ms_to=ts_ms_to):
            sentinel.send(finding)

    if sentinel.failed_sent_events_number:
        logging.error('Script finished unsuccessfully. {} events have been sent. {} events have not been sent'.format(sentinel.successfull_sent_events_number, sentinel.failed_sent_events_number))
        exit(1)
    else:
        logging.info('Script finished successfully. {} events have been sent. {} events have not been sent'.format(sentinel.successfull_sent_events_number, sentinel.failed_sent_events_number))


def convert_datetime_to_ts_ms(dt):
    return int(dt.timestamp() * 1000)


class GuardDutyConnector:
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name):
        self.client = boto3.client(
            'guardduty',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

    def get_findings(self, ts_ms_from=None, ts_ms_to=None):
        for detector_id in self._get_detectors():
            for finding_ids_list in self._get_finding_ids(detector_id=detector_id, ts_ms_from=ts_ms_from, ts_ms_to=ts_ms_to):
                for finding in self._get_findings_by_ids(detector_id=detector_id, finding_ids=finding_ids_list):
                    yield finding

    def _get_detectors(self):
        detectors = []
        try:
            next_token = ''
            while True:
                res = self.client.list_detectors(NextToken=next_token)
                for detector_id in res.get('DetectorIds', []):
                    detectors.append(detector_id)
                next_token = res.get('NextToken', '')
                if not next_token:
                    break
        except Exception as error:
            logging.error('Error during get_detectors - {}'.format(error))
            raise error
        return detectors

    def _get_finding_ids(self, detector_id, ts_ms_from, ts_ms_to):
        finding_criteria = self._construct_finding_criteria(ts_ms_from, ts_ms_to)
        sort_criteria = {
            'AttributeName': 'updatedAt',
            'OrderBy': 'ASC'
        }
        try:
            next_token = ''
            while True:
                res = self.client.list_findings(DetectorId=detector_id, FindingCriteria=finding_criteria, SortCriteria=sort_criteria, NextToken=next_token)
                finding_ids = res.get('FindingIds', [])
                if finding_ids:
                    yield finding_ids
                next_token = res.get('NextToken', '')
                if not next_token:
                    break
        except Exception as error:
            logging.error('Error during list_findings - {}'.format(error))
            raise error

    def _construct_finding_criteria(self, ts_ms_from, ts_ms_to):
        finding_criteria = {}
        if ts_ms_from or ts_ms_to:
            finding_criteria['Criterion'] = dict()
            finding_criteria['Criterion']['updatedAt'] = dict()
            if ts_ms_from:
                finding_criteria['Criterion']['updatedAt']['Gte'] = ts_ms_from
            if ts_ms_to:
                finding_criteria['Criterion']['updatedAt']['Lt'] = ts_ms_to
        return finding_criteria

    def _get_findings_by_ids(self, detector_id, finding_ids):
        sort_criteria = {
            'AttributeName': 'updatedAt',
            'OrderBy': 'ASC'
        }
        try:
            res = self.client.get_findings(DetectorId=detector_id, FindingIds=finding_ids, SortCriteria=sort_criteria)
            for finding in res.get('Findings', []):
                yield finding
        except Exception as error:
            logging.error('Error during get_findings - {}'.format(error))
            raise error
