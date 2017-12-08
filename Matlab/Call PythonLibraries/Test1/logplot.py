import matplotlib.pyplot as plt
import json
import numpy


class LogPlot(object):
    def __init__(self, save_path=None):
        self._save_path = save_path

    def plot(self, structure, save=None):
        if 'TX' in structure:
            self.plot_common_init(structure['TX'], 'Tx', save)

        for ch in ('DACI', 'DACQ'):
            if ch in structure:
                self.dac_initialisation(structure[ch], ch, save)
                self.dac_calibration(structure[ch], ch, save)

        if 'RX' in structure:
            self.plot_common_init(structure['RX'], 'Rx', save)
            try:
                if 'stm_on_lock_status' in structure['RX']:
                    fig = plt.figure()
                    len = numpy.size(numpy.array(structure['RX']['stm_on_lock_status']['even'])) / 2
                    even = numpy.array(structure['RX']['stm_on_lock_status']['even']).reshape((2, len))
                    odd = numpy.array(structure['RX']['stm_on_lock_status']['odd']).reshape((2, len))
                    plt.subplot(1, 2, 1)
                    # plt.plot(numpy.array(structure['RX']['stm_on_lock_status']['even']).reshape((2,len)).T, label='even')
                    plt.plot(even[0], label='EVEN Q')
                    plt.plot(odd[0], label='ODD Q')
                    plt.legend()
                    plt.ylim([0, 63])
                    plt.grid()
                    plt.subplot(1, 2, 2)
                    # plt.plot(numpy.array(structure['RX']['stm_on_lock_status']['odd']).reshape((2,len)).T, label='odd')
                    plt.plot(even[1], label='EVEN I')
                    plt.plot(odd[1], label='ODD I')
                    plt.legend()
                    plt.ylim([0, 63])
                    plt.grid()
                if save:
                    fig.canvas.manager.window.showMaximized()
                    plt.savefig(save + '/phase_align_stm.png')
                    plt.close()
            except Exception as e:
                plt.close()
                print('Error:' + e)
            try:
                if 'lock_status' in structure['RX']:
                    fig = plt.figure()
                    len = numpy.size(numpy.array(structure['RX']['lock_status']['up'])) / 2
                    plt.subplot(2, 1, 1)
                    plt.plot(numpy.array(structure['RX']['lock_status']['up']).reshape((2, len)).T,
                             label='UP')
                    plt.legend()
                    plt.grid()
                    plt.xlim([0, 63])
                    plt.ylim([-0.1, 1.1])
                    plt.subplot(2, 1, 2)
                    plt.plot(numpy.array(structure['RX']['lock_status']['down']).reshape((2, len)).T + 0.05,
                             label='DWN')
                    plt.legend()
                    plt.grid()
                    plt.xlim([0, 63])
                    plt.ylim([-0.1, 1.1])
                if save:
                    fig.canvas.manager.window.showMaximized()
                    plt.savefig(save + '/phase_align_up_dwn.png')
                    plt.close()
            except Exception as e:
                plt.close()
                print(e)
        for ch in ('ADCI', 'ADCQ'):
            if ch in structure:
                self.adc_initialisation(structure[ch], ch, save)
                self.adc_calibration(structure[ch], ch, save)
                self.enob(structure[ch], ch, save)
        plt.show()

    def adc_calibration(self, result, channel, save):
        try:
            iterations = len(result['sampler'])
            sampler_offset = numpy.zeros((iterations, 4))
            sampler_power = numpy.zeros((iterations, 4))
            sampler_dac = numpy.zeros((iterations, 1, 8))

            for i, s in enumerate(result['sampler']):
                sampler_offset[i, :] = s['offset']
                sampler_power[i, :] = s['power']
                sampler_dac[i, :, :] = numpy.array(s['dac_code']).reshape(1, 8)

            # Sampler
            fig = plt.figure()
            plt.subplot(4, 5, 1)
            plt.plot(sampler_offset)
            plt.title('Sampler Offset')

            plt.subplot(4, 5, 2)
            plt.plot(sampler_power)
            plt.title('Sampler Power')

            plt.subplot(4, 5, 3)
            plt.plot(numpy.squeeze(sampler_dac[:, :, :]))
            # plt.plot(sampler_dac[:, 1, :], 'b')
            plt.title('Sampler DACs')
            plt.axis([0, iterations, 0, 255])

            # Sampler Delta & common mode
            plt.subplot(4, 5, 4)
            plt.plot(numpy.squeeze(sampler_dac[:, :, 0::2] - sampler_dac[:, :, 1::2]))
            plt.title('Sampler DACs: N/P Delta')
            plt.axis([0, iterations, -255, 255])

            plt.subplot(4, 5, 5)
            plt.plot(numpy.squeeze(0.5 * (sampler_dac[:, :, 0::2] + sampler_dac[:, :, 1::2])))
            plt.title('Sampler DACs: N/P Common Mode')
            plt.axis([0, iterations, 127 - 32, 127 + 32])

            dmx1_offset = numpy.zeros((iterations, 16))
            dmx1_power = numpy.zeros((iterations, 16))
            dmx1_dac = numpy.zeros((iterations, 16))

            for i, s in enumerate(result['demux1']):
                dmx1_offset[i, :] = s['offset']
                dmx1_power[i, :] = s['power']
                dmx1_dac[i, :] = s['dac_code']

                # DEMUX 1
            plt.subplot(4, 5, 6)
            plt.plot(dmx1_offset)
            plt.title('Demux1 Offset')

            plt.subplot(4, 5, 7)
            plt.plot(dmx1_power)
            plt.title('Demux1 Power')

            plt.subplot(4, 5, 8)
            plt.plot(dmx1_dac)
            plt.title('Demux1 DACs')
            plt.axis([0, iterations, 0, 256])

            dmx2_offset = numpy.zeros((iterations, 64))
            dmx2_power = numpy.zeros((iterations, 64))
            dmx2_dac = numpy.zeros((iterations, 64))

            for i, s in enumerate(result['demux2']):
                dmx2_offset[i, :] = s['offset']
                dmx2_power[i, :] = s['power']
                dmx2_dac[i, :] = s['dac_code']

            # DEMUX 2
            plt.subplot(4, 5, 11)
            plt.plot(dmx2_offset)
            plt.title('Demux2 Offset')

            plt.subplot(4, 5, 12)
            plt.plot(dmx2_power)
            plt.title('Demux2 Power')

            plt.subplot(4, 5, 13)
            plt.plot(dmx2_dac)
            plt.title('Demux2 DACs')
            plt.axis([0, iterations, 0, 256])

            subadc_dac = numpy.zeros((iterations, 12 * 32))
            for i, s in enumerate(result['subadc']):
                subadc_dac[i, :] = s['dac_code']
            subadc_offs = numpy.zeros((iterations, 12 * 32))
            for i, s in enumerate(result['integ_offs']):
                subadc_offs[i, :] = s['offset']
            subadc_power = numpy.zeros((iterations, 12 * 32))
            for i, s in enumerate(result['integ_pwr']):
                subadc_power[i, :] = s['power']

            # SubADC
            plt.subplot(4, 5, 16)
            plt.plot(subadc_offs)
            plt.title('subADC Offset')

            plt.subplot(4, 5, 17)
            plt.plot(subadc_power)
            plt.title('subADC Power')
            plt.axis([0, iterations, 30, subadc_power.max() + 3])

            plt.subplot(4, 5, 18)
            plt.plot(subadc_dac)
            plt.title('subADC DACs')
            plt.axis([0, iterations, 0, 127])

            if save:
                fig.canvas.manager.window.showMaximized()
                plt.savefig(save + '/channel%s_cal.png' % channel)
                plt.close()
        except Exception as e:
            plt.close()
            print(e)

    def adc_initialisation(self, results, channel, save):
        self.phdet16(results, channel, save)
        self.coarse_alignment(results, channel, save)
        self.fine_window(results, channel, save)

        try:
            if 'sadc_vref' in results:
                plt.figure(30)
                plt.plot(results['sadc_vref'], label='VREF %s' % channel)

                if 'sadc_vref_half' in results:
                    plt.plot(results['sadc_vref_half'], ls='-.', label='VREF HALF %s' % channel)

                plt.title('Vref CAL')
                plt.xlabel('REF_ADJ Code')
                plt.ylim([0, 0.8])
                plt.xlim([0, 255])
                plt.legend()
                plt.grid()
                if save:
                    plt.gcf().canvas.manager.window.showMaximized()
                    plt.savefig(save + '/channel%s_vref_cal.png' % channel)
                    plt.close()
        except Exception as e:
            plt.close()
            print(e)

        try:
            if 'clk_data_align' in results:
                plt.figure(30)
                plt.subplot(311)
                plt.plot(results['clk_data_align'], label='clk_data_align %s' % channel)
                plt.title('power sigma')
                plt.xlabel('PI Code')
                plt.xlim([0, 63])
                plt.legend()
                plt.grid()
                if 'up_dwn_status' in results:
                    plt.subplot(312)
                    plt.plot(results['up_dwn_status']['up'], label='up')
                    plt.plot(results['up_dwn_status']['down'], label='dwn')
                    plt.axis([0, 63, -0.1, 1.1])
                    plt.legend()
                    plt.grid()
                    plt.subplot(313)
                    plt.plot(results['up_dwn_status']['odd'], label='odd')
                    plt.plot(results['up_dwn_status']['even'], label='even')
                    plt.axis([0, 63, 0, 63])
                    plt.legend()
                    plt.grid()
                if save:
                    plt.gcf().canvas.manager.window.showMaximized()
                    plt.savefig(save + '/channel%sclk_data_align.png' % channel)
                    plt.close()
        except Exception as e:
            plt.close()
            print(e)

    def plot_common_init(self, results, name, save=None):
        try:
            if 'inductor_sweep' in results:
                plt.figure()
                plt.plot(numpy.array(results['inductor_sweep']).reshape((15, 2)), label=name)
                plt.title('Clock buffer inductor sweep')
                plt.legend()

                if save:
                    plt.gcf().canvas.manager.window.showMaximized()
                    plt.savefig(save + '/inductor_sweep.png')
                    plt.close()
        except Exception as e:
            plt.close()
            print(e)

        try:
            if 'cmfb_sweep' in results:
                plt.figure()
                plt.plot(results['cmfb_sweep'], label=name)
                plt.title('Clock buffer CMFB sweep')
                plt.legend()

                if save:
                    plt.gcf().canvas.manager.window.showMaximized()
                    plt.savefig(save + '/cmfb_sweep.png')
                    plt.close()
        except Exception as e:
            plt.close()
            print(e)

        try:
            if 'cb_sweep' in results:
                plt.figure()
                plt.plot(numpy.array(results['cb_sweep']) * 1.27, label='%s CLOCK p-t * 1.27' % name)
                plt.plot(results['cb_sweep']['cmfb'], label='Clock Amp (clkhi - clklo)')
                plt.plot(results['cb_sweep']['vcm'], label='vcmdriver')
                plt.legend()
                plt.xlabel('Coarse gain')
                plt.ylabel('Voltage')
                if save:
                    plt.gcf().canvas.manager.window.showMaximized()
                    plt.savefig(save + '/cbgain_sweep.png')
                    plt.close()
        except Exception as e:
            plt.close()
            print(e)

        try:
            if 'lock_status' in results:
                plt.figure()
                up = numpy.array(results['lock_status']['up']).reshape((2, 64))
                down = numpy.array(results['lock_status']['down']).reshape((2, 64))
                even = numpy.array(results['lock_status']['even']).reshape((2, 64))
                odd = numpy.array(results['lock_status']['odd']).reshape((2, 64))
                plt.figure()
                plt.title('IQ auto-phase alignment')
                plt.subplot(311)
                plt.axvline(results['lock_status']['rotation'])
                plt.plot(up[0], label='Up Q')
                plt.plot(down[0], label='Down Q')
                plt.axis([0, 63, -0.1, 1.1])
                plt.legend()
                plt.grid()

                plt.subplot(312)
                plt.plot(up[1], label='Up I')
                plt.plot(down[1], label='Down I')
                plt.axis([0, 63, -0.1, 1.1])
                plt.legend()
                plt.grid()

                plt.subplot(313)
                plt.plot(even[0], label='EVEN Q')
                plt.plot(even[1], label='EVEN I')
                plt.plot(odd[0], label='ODD Q')
                plt.plot(odd[1], label='ODD I')
                plt.axis([0, 63, 0, 63])
                plt.legend()
                plt.grid()
                if save:
                    plt.gcf().canvas.manager.window.showMaximized()
                    plt.savefig(save + '/iq_auto_phase_align.png')
                    plt.close()
        except Exception as e:
            plt.close()
            print(e)

        try:
            if 'cb_coarse_sweep' in results:
                plt.figure()
                plt.subplot(211)
                plt.plot(numpy.array(results['cb_coarse_sweep']['regulator']).reshape(15, 4), label='vreg')
                plt.legend()
                plt.grid()
                plt.subplot(212)
                plt.plot(numpy.array(results['cb_coarse_sweep']['swing']).reshape(15, 4), label='clk swing')
                plt.title('Clock buffer coarse gain sweep')
                plt.legend()
                plt.grid()

                if save:
                    plt.gcf().canvas.manager.window.showMaximized()
                    plt.savefig(save + '/cb_coarse_gain_sweep.png')
                    plt.close()
        except Exception as e:
            print(e)

        try:
            if 'cb_fine_sweep' in results:
                plt.figure()
                plt.plot(numpy.array(results['cb_fine_sweep']).reshape(8, 4), label='clk swing')
                plt.legend()
                plt.title('Clock buffer fine gain sweep')
                plt.grid()

                if save:
                    plt.gcf().canvas.manager.window.showMaximized()
                    plt.savefig(save + '/cb_fine_gain_sweep.png')
                    plt.close()
        except Exception as e:
            plt.close()
            print(e)

    def dac_initialisation(self, results, channel, save=None):
        try:
            if 'lsdb_timing' in results:
                plt.figure(10)
                plt.plot(results['lsdb_timing']['dacp'], label='DACP %s' % channel)
                plt.plot(results['lsdb_timing']['dacn'], label='DACN %s' % channel)
                plt.title('LSDB timing')
                plt.xlabel('Delay Code')
                plt.legend()
                #if save:
                    #plt.gcf().canvas.manager.window.showMaximized()
                    #plt.savefig(save + '/lsdb_timing.png')
                    #plt.close()
        except Exception as e:
            plt.close()
            print(e)

        #self.phdet16(results, channel, save)
        #self.coarse_alignment(results, channel, save)
        #self.fine_window(results, channel, save)

    def phdet16(self, results, channel, save):
        try:
            if 'phdet16' in results:
                plt.figure(11)
                plt.plot(results['phdet16'], label='phdet16 %s' % channel)
                plt.title('Phase alignment - detector 16 flag')
                plt.grid()
                plt.xlim(0, 255)
                plt.ylim(-0.1, 1.1)
                plt.legend()
                if save:
                    plt.gcf().canvas.manager.window.showMaximized()
                    plt.savefig(save + "/channel%s_phdet16.png" % channel)
                    plt.close()
        except Exception as e:
            plt.close()
            print(e)

    def coarse_alignment(self, results, channel, save):
        try:
            if 'coarse_alignment' in results:
                plt.figure(12)
                plt.plot(results['coarse_alignment'], label='phdet128 quad %s' % channel)
                plt.title('Coarse alignment')
                plt.grid()
                plt.xlim(0, 31)
                plt.ylim(-0.1, 1.1)
                plt.legend()
                if save:
                    plt.gcf().canvas.manager.window.showMaximized()
                    plt.savefig(save + "/channel%s_alignment_coarse.png" % channel)
                    plt.close()
        except Exception as e:
            plt.close()
            print(e)

    def fine_window(self, results, channel, save):
        try:
            if 'fine_window' in results:
                plt.figure(13)
                plt.plot(numpy.array(results['fine_window']['coarse']) * 64, label='phdet128_quad %s' % channel)
                plt.plot(results['fine_window']['fine'], label='phdet128_fine')
                plt.title('Fine window')
                plt.grid()
                plt.xlim(0, 255)
                plt.ylim(-1, 65)
                plt.legend()
                if save:
                    plt.gcf().canvas.manager.window.showMaximized()
                    plt.savefig(save + '/channel%s_alignment_fine.png' % channel)
                    plt.close()
        except Exception as e:
            plt.close()
            print(e)
        try:
            if 'fine_window' in results:
                plt.figure(14)
                plt.plot((numpy.array(results['fine_window']['fine']) >> 7) * 64, label='phdet128_quad %s' % channel)
                plt.plot(numpy.array(results['fine_window']['fine']) % 128, label='phdet128_fine')
                plt.title('Fine/Coarse window')
                plt.grid()
                plt.xlim(0, 255)
                plt.ylim(-1, 65)
                plt.legend()
                if save:
                    plt.gcf().canvas.manager.window.showMaximized()
                    plt.savefig(save + '/channel%s_alignment.png' % channel)
                    plt.close()
        except Exception as e:
            plt.close()
            print(e)

    def dac_calibration(self, results, channel, save=None):
        if 'current_source' in results:
            self.plot_tail_cal(results['current_source'], results['yoda_cal_dacs'], channel)

        if 'switch' in results:
            self.plot_switch_calibration(results['switch'], results['yoda_cal_dacs'], channel)

    def plot_tail_cal(self, cs, cal_dac, channel):
        try:
            plt.figure()
            plt.title('Current Source Calibration DACs')
            cs = numpy.array(cs)
            iterations = cs.shape[0]
            plt.subplot(211)
            plt.plot((cs[:, 3:] - cs[0, 5:].mean()))
            plt.grid()

            cs_dac = numpy.array([c['current_source'] for c in cal_dac])

            plt.subplot(212)
            plt.plot(cs_dac[:, ::2], 'r', label='Big')
            plt.plot(cs_dac[:, 1::2], 'b', label='Small')
            plt.ylabel('DAC Code')
            plt.xlabel('Iteration')
            handles, labels = plt.gca().get_legend_handles_labels()
            labels, ids = numpy.unique(labels, return_index=True)
            plt.legend([handles[i] for i in ids], labels, loc='best')
            plt.axis([0, iterations, 0, 255])
            plt.grid()
            if self._save_path:
                plt.gcf().canvas.manager.window.showMaximized()
                plt.savefig(self._save_path + '/channel%s_alignment.png' % channel)
                plt.close()
        except:
            pass

    def plot_switch_calibration(self, pulse, cal_dacs, channel):

        try:
            sw_dac = numpy.array([c['switch'] for c in cal_dacs])

            sw_errors = []
            ph_errors = []
            for p in pulse:
                pu = numpy.array(p).reshape(12, 8)[4:, :]
                phase_error = numpy.tile(pu.mean(0).reshape(2, 4).mean(0), (1, 2))
                err = (pu - phase_error)
                sw_errors.append(err)
                ph_errors.append(pu.mean(0) - pu.mean())

            sw_errors = numpy.array(sw_errors)
            ph_errors = numpy.array(ph_errors)
            plt.figure()
            plt.title('Clock switch errors per phase')
            for i in range(8):
                plt.subplot(4, 2, i + 1)
                plt.title('Switch errors for phase %d' % i)
                plt.plot(sw_errors[:, :, i])

            plt.figure()
            plt.title('Clock phase errors')
            lines = plt.plot(ph_errors)
            plt.legend(iter(lines), ('A', 'B', 'C', 'D', '/A', '/B', '/C', '/D'))

            if self._save_path:
                plt.gcf().canvas.manager.window.showMaximized()
                plt.savefig(self._save_path + '/channel%s_alignment.png' % channel)
                plt.close()
        except:
            pass

    def plot_phase_align(self, results, path):
        plt.subplot(4, 1, 1)
        plt.plot(results['channelI']['cd_alignment']['samp_pwr'][1])
        plt.subplot(4, 1, 2)
        if 'channelI' in results:
            plt.plot(results['channelI']['cd_alignment']['filtered_sampler_power']['filtered'])
        if 'channelQ' in results:
            plt.plot(results['channelQ']['cd_alignment']['filtered_sampler_power']['filtered'])
        plt.subplot(4, 1, 3)
        if 'channelI' in results:
            plt.plot(results['channelI']['cd_alignment']['samp_pwr_abcd'][:])
        if 'channelQ' in results:
            plt.plot(results['channelQ']['cd_alignment']['samp_pwr_abcd'][:])
        plt.subplot(4, 1, 4)
        if 'channelI' in results:
            plt.plot(results['channelI']['cd_alignment']['sigma'][:])
        if 'channelQ' in results:
            plt.plot(results['channelQ']['cd_alignment']['sigma'][:])
        plt.gcf().canvas.manager.window.showMaximized()
        plt.savefig(path + '/sw_phase_align.png')
        plt.close()

        import numpy
        plt.subplot(5, 1, 2)
        sampler_power_sigma_fit = numpy.zeros((2, 64))
        if 'channelI' in results:
            sampler_power_sigma_fit[0, :] = results['channelI']['cd_alignment']['filtered_sampler_power_sigma'][
                'filtered']
            plt.plot(sampler_power_sigma_fit[0, :], label='I')
        if 'channelQ' in results:
            sampler_power_sigma_fit[1, :] = results['channelQ']['cd_alignment']['filtered_sampler_power_sigma'][
                'filtered']
            plt.plot(sampler_power_sigma_fit[1, :], label='Q')
        plt.xlim(([0, 63]))
        plt.legend()
        plt.grid()
        plt.subplot(5, 1, 1)
        plt.plot(numpy.sum(sampler_power_sigma_fit, 0), label='pwr sigma')
        plt.xlim(([0, 63]))
        plt.legend()
        plt.grid()
        plt.subplot(5, 1, 3)
        if 'channelI' in results:
            plt.plot(results['channelI']['cd_alignment']['pi_status']['up'], label='I up')
        if 'channelQ' in results:
            plt.plot(results['channelQ']['cd_alignment']['pi_status']['up'], label='Q up')
        plt.xlim(([0, 63]))
        plt.ylim(([-0.1, 1.1]))
        plt.legend()
        plt.grid()
        plt.subplot(5, 1, 4)
        if 'channelI' in results:
            plt.plot(results['channelI']['cd_alignment']['pi_status']['down'], label='I dwn')
        if 'channelQ' in results:
            plt.plot(results['channelQ']['cd_alignment']['pi_status']['down'], label='Q dwn')
        plt.xlim(([0, 63]))
        plt.ylim(([-0.1, 1.1]))
        plt.legend()
        plt.grid()
        plt.subplot(5, 1, 5)
        if 'channelI' in results:
            plt.plot(results['channelI']['cd_alignment']['pi_status']['even'], label='I even')
            plt.plot(results['channelI']['cd_alignment']['pi_status']['odd'], label='I odd')
        if 'channelQ' in results:
            plt.plot(results['channelQ']['cd_alignment']['pi_status']['even'], label='Q even')
            plt.plot(results['channelQ']['cd_alignment']['pi_status']['odd'], label='Q odd')
        plt.xlim(([0, 63]))
        plt.ylim(([0, 63]))
        plt.legend()
        plt.grid()
        plt.gcf().canvas.manager.window.showMaximized()
        plt.savefig(path + '/sw_phase_align_sigma.png')
        plt.close()

    def enob(self, results, channel, save):
        if 'wavemem' in results:
            data = numpy.array([])
            for w in results['wavemem']:
                data = numpy.append(data, w['data'])

            import enob
            data = (data - 128) % 256
            adc_fft_db, enob_, enob2, freq_harm, ampl_harm, freq_spur, ampl_spur, thd, snr = enob.wintru_spurs2(data,
                                                                                                                do_window=1)
            enob.plot_enob(data, adc_fft_db, freq_harm, ampl_harm, freq_spur, ampl_spur, enob2, thd, snr)


if __name__ == '__main__':
    d = json.load(open(r'corellian_74G.log'))

    pl = LogPlot('./')
    pl.plot(d)

    print 'done'
