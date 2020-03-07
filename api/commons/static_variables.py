from api.resources.company import Company
import secrets
from api.resources.structures import TerminalText

TEAM_MAPPER = Company.export_team_links_to_dict()
TERM_TEXT = TerminalText()
CUR_VIDEO = dict()
OPTIONS = dict()


def generate_user_id():
    secret_token = secrets.token_hex(15)
    return secret_token
