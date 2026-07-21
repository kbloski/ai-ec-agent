from enum import Enum


class ExperimentType(str, Enum):
    ANGLE = "ANGLE"
    MESSAGE = "MESSAGE"
    AUDIENCE = "AUDIENCE"
    OFFER = "OFFER"
    CREATIVE = "CREATIVE"
    HOOK = "HOOK"
    CTA = "CTA"
    PROOF = "PROOF"
