#!/usr/bin/python
#

try:
    import gdb
except ImportError as e:
    raise ImportError("This script must be run in GDB: ", str(e))
import sys
import os
sys.path.append(os.getcwd())
import common_helpers


simple_types = ["CMasternode", "CMasternodeVerification",
                "CMasternodeBroadcast", "CMasternodeIndex", "CMasternodePing",
                "CMasternodeMan", "CDarksendQueue", "CDarkSendEntry",
                "CTransaction", "CMutableTransaction", "CPrivateSendBase",
                "CPrivateSendClient", "CPrivateSendServer", "CMasternodePayments",
                "CMasternodePaymentVote", "CMasternodeBlockPayees",
                "CMasternodePayee", "CInstantSend", "CTxLockRequest",
                "CTxLockVote", "CTxLockCandidate", "COutPoint", "CTxLockRequest",
                "COutPointLock", "CSporkManager", "CMasternodeSync",
                "CGovernanceManager", "CRateCheckBuffer", "CGovernanceObject",
                "CGovernanceVote", "CGovernanceObjectVoteFile"]

simple_templates = ["CacheMultiMap", "CacheMap"]


class SimpleClassObj:

    def __init__ (self, obj_name, obj_type):
        self.obj_name = obj_name
        self.obj_type = obj_type

    @classmethod
    def is_this_type(cls, obj_type):
        str_type = str(obj_type)
        if str_type in simple_types:
            return True
        for templ in simple_templates:
            if str_type.find(templ + "<") == 0:
                return True
        return False

    def get_used_size(self):
        print("process %s of type %s" % (self.obj_name, str(self.obj_type)))
        size = 0
        fields = self.obj_type.fields()
        for f in fields:
            # check if it is static field
            if not hasattr(f, "bitpos"):
                continue
            # process base class size
            if f.is_base_class:
                size += common_helpers.get_instance_size(self.obj_name, f.type)
                continue
            # process simple field
            size += common_helpers.get_instance_size("(" + self.obj_name + ")." + f.name, f.type)
        print("used size is %d" % size)
        return size
