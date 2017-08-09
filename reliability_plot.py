###############################################################################
# File         : reliability_plot.py
# Author       : Neil Massey
# Created      : 02/06/11
# Purpose      : Reliability diagram
###############################################################################

import matplotlib.pyplot as plt
import numpy
from calc_dichot_event_bins import *

###############################################################################

def format_reliability_plot(plt_o, prob_bins):
	# draw the one to one line
	plt_o.plot([0,1],[0,1], 'k', lw=2.0)
	# set the axis and labels
	plt_o.set_xlabel("Forecast probability")
	plt_o.set_ylabel("Relative observed frequency")
	plt_o.set_xlim([0,1.0])
	plt_o.set_ylim([0,1.0])
	# set the xticks / labels
	x_ticks = numpy.arange(0, 1.05, 0.05)
	plt_o.set_xticks(x_ticks)
	x_tick_labels = []
	for x in range(0, len(x_ticks)):
		if x_ticks[x] in prob_bins:
			x_tick_labels.append(x_ticks[x])
		else:
			x_tick_labels.append("")
	plt_o.set_xticklabels(x_tick_labels)
	# have the same ticks for the y range
	plt_o.set_yticks(x_ticks)
	plt_o.set_yticklabels(x_tick_labels)
	plt_o.set_title("Reliability")

###############################################################################

def format_sharpness(plt_shrp, prob_bins, prob_count, shrp_max, draw_x_ticks=False, 
					 draw_y_ticks=False):
	bw = prob_bins[1] - prob_bins[0]
	plt_shrp.set_xticks(prob_bins)
	if draw_x_ticks:
		xticks = []
		for i in range(0, len(prob_bins)):
			if i % 2 == 0:
				xticks.append(str(prob_bins[i]))
			else:
				xticks.append("")
		plt_shrp.set_xticklabels(xticks)
	else:
		plt_shrp.set_xticklabels(["" for x in range(0, len(prob_bins))])
	plt_shrp.set_yticks([y for y in range(0, shrp_max, shrp_max / 5)])
	if not draw_y_ticks:
		plt_shrp.set_yticklabels(["" for x in range(0, len(prob_bins))])
	plt_shrp.set_ylim([0, shrp_max])
	plt_shrp.set_xlim([-0.5*bw, 1.0+0.5*bw])

###############################################################################

def reliability_plot(obs, forc, thresh_fn, obs_thresh_val, forc_thresh_val=None, bw=0.1):
	# inputs : plt_o 	 : plot object
	#          obs   	 : vector (1D numpy array) of observed values
	#          forc  	 : matrix (2D numpy array) of forecast values - an ensemble member per row
	#		   thresh_fn : thresholding function to set obs / forc to 0 or 1
	#		   thresh_val : value to use in the thresholding function
	#		   bw         : bin width for probability bins

	plt_o = plt.subplot(1,2,1)

	# generate the data for the reliability plot
	prob_bins, obs_freq, bin_count = calc_dichot_event_bins(obs, forc, thresh_fn, obs_thresh_val, 
											forc_thresh_val, bw)

	# plot each observed frequency / forecast probability pair
	c = 'b'
	plt_idx = numpy.where(bin_count != 0)
	plt_o.plot(prob_bins[plt_idx], obs_freq[plt_idx], c+"o", mew=0.2)		# plot the points as "o"s
	# plot the line
	l1 = plt_o.plot(prob_bins[plt_idx], obs_freq[plt_idx], c+"-", lw=2.0)
	format_reliability_plot(plt_o, prob_bins)

	# draw the no skill and no resolution line
	d_bar = numpy.sum(bin_count*obs_freq) / numpy.sum(bin_count)
	plt_o.plot([0.0, 1.0], [d_bar, d_bar], 'k--')	# no resolution line
	no_res_y = [(prob_bins[i] + d_bar)/2.0 for i in range(0, prob_bins.shape[0])]
	plt_o.plot(prob_bins, no_res_y, 'k-.')

	# plot sharpness
	plt_shrp = plt.subplot(1,2,2)
	ww = 0.01
	plt_shrp.bar(prob_bins+ww, bin_count, width=bw-2*ww, ec=c, fc=c)
	mc = numpy.max(bin_count)
	format_sharpness(plt_shrp, prob_bins, bin_count, mc, True)
	plt_shrp.set_xlabel("Probability bin")
	plt_shrp.set_ylabel("Frequency")
	plt_shrp.set_title("Bin Frequency")
	plt_o.set_aspect(1.0)
	plt_shrp.set_aspect(1.0/mc)
	plt_o.set_position(pos=[0.1, 0.0, 0.35, 1.0])    # [l b w h]
	plt_shrp.set_position(pos=[0.55, 0.0, 0.39, 1.0])

###############################################################################

def multi_reliability_plot(obs, forc, thresh_fn, obs_thresh_vals, forc_thresh_vals=None, ptile_vals = None, bw=0.1):
	# inputs : plt_o 	   : plot object
	#          obs   	   : vector (1D numpy array) of observed values
	#          forc  	   : matrix (2D numpy array) of forecast values - an ensemble member per row
	#		   thresh_fn   : thresholding function to set obs / forc to 0 or 1
	#		   thresh_vals : threshold values
	#		   ptile_vals  : list of percentiles to use in the thresholding function
	#		   bw          : bin width for probability bins
	sp1 = plt.subplot2grid((2,4), (0,0), colspan=2, rowspan=2)

	# generate the data for the reliability plot
	lines = []
	colours = ['b', 'r', 'g', 'k', 'c']
	prob_bin_1 = []		# maintain the scope
	prob_counts = []
	if forc_thresh_vals == None:
		forc_thresh_vals = obs_thresh_vals
	# perfect data
	p_forc = forc[0]
	for i in range(0, len(obs_thresh_vals)):
		prob_bin_1, obs_freq_1, prob_count_1 = calc_dichot_event_bins(obs, forc, thresh_fn, obs_thresh_vals[i], forc_thresh_vals[i], bw)
		# perfect data
		prob_bin_p, obs_freq_p, prob_count_p = calc_dichot_event_bins(p_forc, forc, thresh_fn, forc_thresh_vals[i], forc_thresh_vals[i], bw)
		# plot each point and line if the bin count is not 0
		c = colours[i % len(colours)]
		plt_idx = numpy.where(prob_count_1 != 0)
		sp1.plot(prob_bin_1[plt_idx], obs_freq_1[plt_idx], c+'o', mew=0.2, mfc=c, mec=c)	# plot the points as "o"s
		l_1 = sp1.plot(prob_bin_1[plt_idx], obs_freq_1[plt_idx], c+'-', lw=2.0)	# plot the line
		plt_idx = numpy.where(prob_count_p != 0)
		sp1.plot(prob_bin_p[plt_idx], obs_freq_p[plt_idx], c+'o', mew=0.2, mfc=c, mec=c)	# plot the points as "o"s
		sp1.plot(prob_bin_p[plt_idx], obs_freq_p[plt_idx], c+'--', lw=2.0)	# plot the line
		lines.append(l_1[0])	# save the line for the legend
		prob_counts.append(prob_count_1)	# needed for sharpness diagrams
		# calculate and print the Brier Score
		brier_score = True
		if brier_score:
			bs_squared = numpy.square(numpy.array(prob_bin_1) - numpy.array(obs_freq_1))
			bs_forc_obs = 1.0 / len(prob_bin_1) * numpy.sum(bs_squared)
			print ptile_vals[i], "Ens vs Obs", bs_forc_obs
			bs_squared_p = numpy.square(numpy.array(prob_bin_p) - numpy.array(obs_freq_p))
			bs_forc_obs_p = 1.0 / len(prob_bin_p) * numpy.sum(bs_squared_p)
			print ptile_vals[i], "Ens vs Ens", bs_forc_obs_p
	format_reliability_plot(sp1, prob_bin_1)

	# draw the legends
	if ptile_vals != None:
		plt.legend(lines, ptile_vals, loc='upper left', title="Percentile of observation", ncol=2)

	# now draw the sharpness diagrams
	n_shrp_dias = len(obs_thresh_vals)
	# set the subplots up
	ww = 0.025
	shrp_sp = []
	shrp_max = 0
	x_pos = [2,3,2,3]
	y_pos = [0,0,1,1]

	for i in range(0, n_shrp_dias):
		sp2 = plt.subplot2grid((2,4),(y_pos[i],x_pos[i]))
		shrp_sp.append(sp2)
		shrp_sp[-1].bar(prob_bin_1-ww*0.5, prob_counts[i], width=ww, ec=colours[i], fc=colours[i])
		shrp_max_1 = 50 * int(numpy.max(prob_counts[i]) / 50) + 50
		if shrp_max_1 > shrp_max:
			shrp_max = shrp_max_1

	for i in range(0, n_shrp_dias):
		format_sharpness(shrp_sp[i], prob_bin_1, prob_counts[i], shrp_max,
						 (i==2) | (i==3), (i==0) | (i==2))
	shrp_sp[0].set_ylabel("# of samples")
	shrp_sp[2].set_ylabel("# of samples")

###############################################################################

if __name__ == "__main__":
	obs  = numpy.array( [0.6, 0.0, 0.0, 0.0, 0.6, 0.0, 0.6, 0.6, 0.6, 0.0, 0.6], 'f' )

# 	perfect data
	forc = numpy.array([[0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6],
	                    [0.0, 0.0, 0.0, 0.0, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6],
	                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6, 0.6, 0.6, 0.6, 0.6],
	                    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.6]], 'f')

	reliability_plot(obs, forc, thresh_gt_score, 0.5, 0.25)
	plt.show()
