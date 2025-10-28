import config
import oracledb
import psutil

logger = config.logger

def get_service_status(service_name):
    """
    Checks the status of a Windows service.

    Args:
        service_name (str): The name of the Windows service.

    Returns:
        str: The status of the service (e.g., 'running', 'stopped', 'paused'),
             or 'not found' if the service does not exist.
    """
    try:
        service = psutil.win_service_get(service_name)
        service_info = service.as_dict()
        return service_info['status']
    except psutil.NoSuchProcess:
        logger.error(f"Service not found: {service_name}")
        return 'not found'
    except Exception as e:
        logger.error(f"An error occurred when checking service ({service_name}): {e}")
        return 'error'

def get_all_statuses(db_conn: oracledb.Connection):
    return [
        get_da_internal_status(),
        get_crm_messenger_status(),
        get_crm_webapi_status(),
        get_stuck_jobs_status(db_conn),
    ] + get_daily_checks_statuses()

def get_status_info(id, display, type, status, details=None):
    return {
        "id": id,
        "display_name": display,
        "type": type,
        "status": status,
        "status_details": details
    }

def get_crm_messenger_status():
    service_name_to_check = "CRMMessenger_CXDEV"
    status = get_service_status(service_name_to_check)
    status_info = get_status_info (
        "CRMMessenger",
        "CRM Messenger Windows Service",
        "service",
        status)
    return status_info

def get_crm_webapi_status():
    status = 'running'
    status_info = get_status_info (
        "CRMWebAPI",
        "CRM Web API",
        "webapi",
        status)
    return status_info

def get_da_internal_status():
    status = 'running'
    status_info = get_status_info (
        "DAInternal",
        "Direct Access Internal Website",
        "website",
        status)
    return status_info

def get_stuck_jobs_status(db_conn: oracledb.Connection):
    # HERE: Make call to DB to check for potentially stuck job
    # Sample Call to Oracle DB

    items = []
    cursor = None
    try:
        cursor = db_conn.cursor()
        cursor.execute("SELECT 1, 'test' FROM dual")
        rows = cursor.fetchall()
        items = [{"id": row[0], "name": row[1]} for row in rows]
    finally:
        if cursor:
            cursor.close()


    # For now, lets return some mock data so the project can run successfully out of the box.
    status = 'warning' if len(items) > 0 else 'failed'
    details = '''Process DCMD Records: Processing since Wednesday October 22, 2025 1:08 pm on Fourth Server
Attach latest Transcript: Processing since Wednesday October 22, 2025 3:14 pm on Second Server'
Send Immediate Emails: Processing since Wednesday October 22, 2025 4:01 pm on Third Server'''
    status_info = get_status_info (
        "StuckJobs",
        "Stuck Scheduled Jobs",
        "process",
        status,
        details)
    return status_info

def get_daily_checks_statuses():
    # HERE: Make call to DB to get the daily checked statuses.
    # For now, lets return some mock data so the project can run successfully out of the box.
    return [
        get_status_info (
            "Batch_Email",
            "Overnight Batch - Email",
            "batch",
            "failed",
            "Error when performing check: ORA-01422: exact fetch returns more than requested number of rows"
        ),
        get_status_info (
            "Batch_LINRegCard",
            "Overnight Batch - LIN Registration Card",
            "batch",
            "ok"
        ),
        get_status_info (
            "CRMMessengerQueue",
            "CRM Messenger Queue < 1000",
            "process",
            "ok"
        )
    ]
