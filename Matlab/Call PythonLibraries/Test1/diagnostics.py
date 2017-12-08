#import serial
import json


class Diagnostics(object):
    def __init__(self):
        self.results = {}

    def create_or_append(self, name, data, item):
        if name in data:
            if name not in item:
                item[name] = []
            item[name].append(data[name])
            return True
        return False

    def process_line(self, line):
        if 'DATA' not in line:
            return

        context = line.split()[2].strip('>')
        if context not in self.results:
            self.results[context] = dict()
        try:
            data = json.loads(line.split(' - ')[1])
            handled = False
            handled |= self.create_or_append('yoda_cal_dacs', data, self.results[context])
            handled |= self.create_or_append('current_source', data, self.results[context])
            handled |= self.create_or_append('switch', data, self.results[context])
            handled |= self.create_or_append('sampler', data, self.results[context])
            handled |= self.create_or_append('demux1', data, self.results[context])
            handled |= self.create_or_append('demux2', data, self.results[context])
            handled |= self.create_or_append('subadc', data, self.results[context])
			#handled |= self.create_or_append('integ_offs', data, self.results[context])
    	    #handled |= self.create_or_append('integ_pwr', data, self.results[context])
	        #handled |= self.create_or_append('wavemem', data, self.results[context])
            #handled |= self.create_or_append('eq_gain', data, self.results[context])
            #handled |= self.create_or_append('eq_offset', data, self.results[context])
            #handled |= self.create_or_append('bit_power', data, self.results[context])
            #handled |= self.create_or_append('link_snr', data, self.results[context])

            if not handled:
                self.results[context].update(data)
        except:
            pass



    def from_file(self, path):
        with open(path) as fid:
            for line in fid:
                self.process_line(line)

        return self.results


if __name__ == '__main__':
    import sys
    from logplot import LogPlot
    import ast
    import argparse

    parser = argparse.ArgumentParser(description='plot log results')
    parser.add_argument('--root', dest='root', help='path to save log file')

    args = parser.parse_args()
    if args.root is not None:
        diagnostics = Diagnostics()
        results = diagnostics.from_file(args.root+'\\corellian.log')
        LogPlot().plot(results, args.root+'\\download\\')
    else:
        diagnostics = Diagnostics()
        results = diagnostics.from_file('C:\\Users\\fcarmo_lab\\Desktop\\projects\\16ff\\measdata\\temp\\MACE_bench1_B0\\MACE_LH_L\\TT27\\fs_46.00\\temp_25\\v_mid\\20170906_0839_8bit_fullrate\\corellian.log')
        LogPlot().plot(results, './results')