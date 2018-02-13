# federal money module
import datetime


class FedDonor:

    def __init__(self):
        self.lastdonation = ''

    # return true/false if donation represents "repeat"
    # repeat is only counted if we know of an earlier donation
    def add_donation(self, trans_dt):
        assert isinstance(trans_dt, datetime.datetime)

        # this is the first recorded donation
        if self.lastdonation == '':
            self.lastdonation = trans_dt
            return False

        # if the last donation was this or a previous year,
        # then it was a repeat. If it is later (>) then it
        # was very out of order so ignore
        if self.lastdonation.year <= trans_dt.year:
            return True
        else:
            # otherwise, record new, even earlier donation
            # (just in case we get further out-of-order data)
            self.lastdonation = trans_dt
            return False
