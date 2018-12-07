from integrations.call_center import call_center
from api.call.business_logics import call_bl

if __name__ == '__main__':
    call_center.listen_log(call_bl.update_call)
