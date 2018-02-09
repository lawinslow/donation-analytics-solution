import csv
import sys
import os
import datetime
import numpy as np

# define our default values and indices
expec_col = 21
quantile = 1
indx_cmte_id = 0
indx_name = 7
indx_zip = 10
indx_trans_date = 13
indx_trans_amt  = 14
indx_other_id = 15
datetime_fmt = '%m%d%Y'

# dictionaries to keep track of donors/recipients
donors = dict()
recipients = dict()

# open all files
f_input = open('input/itcont.txt')


# check all the input parameters for valid range/value
if quantile < 1 or quantile > 100:
    sys.exit(1, 'Quantile input file must contain number between 1 and 100')


data_csv = csv.reader(f_input, delimiter='|')

for row in data_csv:

    # first row quality checks, expected col n and 'other_id' col
    if len(row) != expec_col:
        print('Continuing...')
        continue
    if row[indx_other_id].strip():
        print('Skipping as other_id is not empty')
        continue

    trans_dt = datetime.datetime.strptime(row[indx_trans_date], datetime_fmt)
    zip_trunc = row[indx_zip][0:5]
    trans_amt = int(round(float(row[indx_trans_amt])))
    donor_name = row[indx_name]
    recip_id = row[indx_cmte_id]

    #print("CMTE_ID:", )
    #print("NAME:", donor_name)
    #print("ZIP_CODE:", zip_trunc)
    #print("TRANSACTION_DT:", trans_dt)
    #print("TRANSACTION_AMT:", trans_amt)
    #print("OTHER_ID:", row[indx_other_id])


    is_repeat = (donor_name + zip_trunc) in donors
    donors[(donor_name + zip_trunc)] = True

    #print(is_repeat)
    #print("\n")

    if is_repeat:
        urid = recip_id + zip_trunc + str(trans_dt.year)

        if urid not in recipients:
            recipients[urid] = list()

        recipients[urid].append(trans_amt)

        medval = np.percentile(recipients[urid], quantile, interpolation='lower')
        sumval = np.sum(recipients[urid])
        nval   = len(recipients[urid])

        print(recip_id, '|', zip_trunc, '|', trans_dt.year, '|', medval, '|', nval)



# cleanup files
f_input.close()