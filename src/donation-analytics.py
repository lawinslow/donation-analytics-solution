import csv
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
import datetime
import numpy as np
import fedmoney

# define our default values and indices
expec_col = 21    #Number of columns expected for each row
indx_cmte_id = 0
indx_name = 7
indx_zip = 10
indx_trans_date = 13
indx_trans_amt  = 14
indx_other_id = 15
datetime_fmt = '%m%d%Y'

def main(argv):

    percentile_val = -1
    # dictionaries to keep track of donors/recipients
    donors           = dict()
    recipients       = dict()
    input_fname      = 'input/itcont.txt'
    output_fname     = 'output/repeat_donors.txt'
    percentile_fname = 'input/percentile.txt'
    input_rownum     = 0

    if len(argv) < 2 or len(argv) > 4:
        sys.stderr.write('Error: Unknown parameters supplied. Three expected.\n')
        sys.stderr.write('Usage: donation-analytics.py <input file> <*output file> <*percentile file>\n' +
                         '* Optional parameter defaults\n' +
                         'output file: output/repeat_donors.txt\n' +
                         'percentile file: input/percentile.txt\n\n')
        sys.exit(1)

    if len(argv) >= 2:
        input_fname = argv[1]
    if len(argv) >= 3:
        output_fname = argv[2]
    if len(argv) == 4:
        percentile_fname = argv[3]




    try:
        # open all files
        f_input = open(input_fname, 'r')
        f_output = open(output_fname, 'w')
        f_percentile = open(percentile_fname, 'r')

        percentile_val = int(f_percentile.readline().strip())

    except IOError:
        sys.stderr.write('Trouble opening input and output files, please verify files:')
        sys.stderr.writelines('Input file:' + input_fname)
        sys.stderr.writelines('Output file:' + output_fname)
        sys.stderr.writelines('Percentile file:' + percentile_fname)
        sys.exit(1)

    except ValueError:
        sys.stderr.writelines('Problem reading percentile value.')
        sys.stderr.writelines('Please verify percentile file:', + percentile_fname)
        sys.exit(1)

    # check all the input parameters for valid range/value
    if percentile_val < 1 or percentile_val > 100:
        sys.stderr.write('Percentile input file must contain number between 1 and 100')
        sys.exit(1)

    data_csv = csv.reader(f_input, delimiter='|')

    for row in data_csv:
        #increment row counter
        input_rownum += 1

        # first row quality checks, expected col n and 'other_id' col
        if len(row) != expec_col:
            sys.stderr.write(str(input_rownum) + '# line: Skipping line due to invalid column count\n')
            continue
        if row[indx_other_id].strip():
            # this is a common occurrence, do not report
            continue

        try:
            trans_dt = datetime.datetime.strptime(row[indx_trans_date], datetime_fmt)
        except ValueError:
            # write line number and skip to next line, don't know date order if missing date
            sys.stderr.write(str(input_rownum) + '# line: Problem parsing datetime\n')
            continue


        zip_trunc = row[indx_zip][0:5]
        trans_amt = int(round(float(row[indx_trans_amt])))
        donor_name = row[indx_name]
        recip_id = row[indx_cmte_id]

        if (donor_name + zip_trunc) not in donors:
            donors[(donor_name + zip_trunc)] = fedmoney.FedDonor()

        is_repeat = donors[(donor_name + zip_trunc)].add_donation(trans_dt)

        if is_repeat:
            urid = recip_id + zip_trunc + str(trans_dt.year)

            if urid not in recipients:
                recipients[urid] = list()

            recipients[urid].append(trans_amt)

            medval = str(np.percentile(recipients[urid], percentile_val, interpolation='lower'))
            sumval = str(np.sum(recipients[urid]))
            nval   = str(len(recipients[urid]))

            f_output.write(recip_id + '|' + zip_trunc + '|' +
                           str(trans_dt.year) + '|' + medval + '|' +
                           sumval + '|' + nval + '\n')

    # cleanup files
    f_input.close()
    f_output.close()


if __name__ == "__main__":
    main(sys.argv)
