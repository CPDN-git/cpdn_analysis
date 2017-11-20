###############################################################################
# File         : q_q_plot.py
# Author       : Neil Massey
# Created      : 11/08/11
# Purpose      : Plot non-conditional quantiles
###############################################################################

import matplotlib.pyplot as plt
from scipy import stats
import numpy
import random

###############################################################################

def q_q_plot(obs, ens, p_tiles):
	sp = plt.subplot(111)
	# plot the (non-conditional) quantiles
	obs_quantiles = []
	ens_quantiles = []
	for i in range(1, 99):
		obs_quantiles.append(stats.scoreatpercentile(obs.flatten(), i))
		ens_quantiles.append(stats.scoreatpercentile(ens.flatten(), i))
	sp.plot(obs_quantiles, ens_quantiles, 'k--', lw=1.5, zorder=1)
	ens_range = ens_quantiles[-1] - ens_quantiles[0]
	# plot the percentiles in the p_tiles list)
	for p in p_tiles:
		obs_p = stats.scoreatpercentile(obs.flatten(), p)
		ens_p = stats.scoreatpercentile(ens.flatten(), p)
		sp.plot(obs_p, ens_p, 'k+', ms=12, zorder=1)
		sp.text(obs_p, ens_p-0.05*ens_range, str(p), ha='center', va='bottom',
				zorder=1)

	smallest_x = numpy.min([obs_quantiles[0], ens_quantiles[0]])
	largest_x = numpy.max([obs_quantiles[-1], ens_quantiles[-1]])

	# 1:1 line - lowest z order
	sp.plot([smallest_x, largest_x], [smallest_x, largest_x], 'k', lw=2.0,
			zorder=0)
	# limits
	sp.set_xlim([smallest_x, largest_x])
	sp.set_ylim([smallest_x, largest_x])
	sp.set_aspect(1.0)
	return sp

###############################################################################

def multi_q_q_plot(plt_obj, obs, ens, line_shp=['--', '-', '-.-'], colors=['r','b','c'], p_tiles=[5,10,50,90,95], lw=1.0):
	# multiple data version of q-q plot
	# number of observations and ensemble members
	n_dsets = len(obs)
	if n_dsets != len(ens):
		raise("Observations and Ensembles do not have the same number of datasets to plot")

	# calculate the percentiles
	min_val = 2e20
	max_val = -2e20
	lines = []
	for n in range(0, n_dsets):
		obs_quantiles = []
		ens_quantiles = []
		for i in range(1, 99):
			obs_quantiles.append(stats.scoreatpercentile(obs[n].flatten(), i))
			ens_quantiles.append(stats.scoreatpercentile(ens[n].flatten(), i))
		l = plt_obj.plot(obs_quantiles, ens_quantiles, color=colors[n], ls=line_shp[n], 
						 lw=lw, zorder=1)
		lines.append(l[0])
		ens_range = ens_quantiles[-1] - ens_quantiles[0]
		# plot the percentiles in the p_tiles list)
		if n == 1:
			for p in p_tiles:
				obs_p = stats.scoreatpercentile(obs[n].flatten(), p)
				ens_p = stats.scoreatpercentile(ens[n].flatten(), p)
				plt_obj.plot(obs_p, ens_p, color= colors[n], marker='s', ms=4, 
							 mec=colors[n], zorder=1)
				plt_obj.text(obs_p, ens_p+0.05*ens_range, str(p), ha='center', va='bottom', 
							 color='k', zorder=1)#colors[n])
		# keep a record of the min and max value
		min_val = numpy.min([obs_quantiles[0], ens_quantiles[0], min_val])
		max_val = numpy.max([obs_quantiles[-1], ens_quantiles[-1], max_val])

	# 1:1 line - lowest z order
	plt_obj.plot([min_val, max_val], [min_val, max_val], 'k', lw=2.0, 
				  zorder=0)
	# limits
	plt_obj.set_xlim([min_val, max_val])
	plt_obj.set_ylim([min_val, max_val])
	plt_obj.set_aspect(1.0)
	return lines

###############################################################################

def q_q_plot_confidence(obs, ens, p_tiles, colors=['r'], bsn=1e5):
	# produce a quantile quantile plot with confidence limits between 5th and 95th
	# percentile of the percentile value
	# ens can be a list for multiple values
	# bsn = boot strap sample number
	# create the plot
	sp = plt.subplot(111)

	# calculate the observed percentiles first
	obs_quantiles = []
	obs_f = obs.flatten()
	obs_f.sort()
	# loop through the 1st to 99th percentile
	for pt in range(1, 99):
		# get the observed scoreatpercentile for this percentile
		obs_quantiles.append(stats.scoreatpercentile(obs_f, pt))

	c = 0
	legend_lines = []
	for n in range(0, len(ens)):
		e = ens[n]
		# create the storage
		ens_quantiles = []
		ens_quantiles_5th = []
		ens_quantiles_50th = []
		ens_quantiles_95th = []

		# flattened observation and ensemble
		ens_f = e.flatten()
		ens_f.sort()
		# number of ensemble members
		ens_n = e.shape[0]

		# create the sample indices
		# this ensures we sample the same ensemble member for each percentile
		sample_idx = []
		for bn in range(0, bsn):
			si = int(random.uniform(0, ens_n))
			sample_idx.append(si)

		# loop through the 1st to 99th percentile
		for pt in range(1, 99):
			# build up a sample set by sampling each ensemble member - with replacement
			ens_samples = []
			for bn in range(0, bsn):
				idx = sample_idx[bn]		# get a random ensemble member
				member_data = e[idx]
				# get the percentile score and add it to the ens_samples
				v = stats.scoreatpercentile(member_data, pt)
				ens_samples.append(v)
			# get the 5th, 50th and 95th percentile of these values
			ens_quantiles_5th.append(stats.scoreatpercentile(ens_samples, 5))
			ens_quantiles_50th.append(stats.scoreatpercentile(ens_samples, 50))
			ens_quantiles_95th.append(stats.scoreatpercentile(ens_samples, 95))
			# add the actual ensemble variable
			ens_quantiles.append(stats.scoreatpercentile(ens_f, pt))

		# plot the actual ensemble vs observations quantiles
		l = sp.plot(obs_quantiles, ens_quantiles, ls='-', c=colors[c], lw=1.5, zorder=1)
		legend_lines.append(l[0])

		sp.fill_between(obs_quantiles, ens_quantiles_5th, ens_quantiles_95th, 
						facecolor=colors[c], edgecolor=colors[c], alpha=0.75)
		# plot the percentiles in the p_tiles list)
		ens_range = ens_quantiles[-1] - ens_quantiles[0]
		if n == 1:	# only do one
			for p in p_tiles:
				obs_p = stats.scoreatpercentile(obs.flatten(), p)
				ens_p = stats.scoreatpercentile(e.flatten(), p)
				sp.plot(obs_p, ens_p, mfc=colors[c], mec=colors[c], marker='s', ms=4, zorder=1)
				if c % 2 == 0:
					vp = ens_p - 0.035*ens_range
				else:
					vp = ens_p + 0.035*ens_range
				sp.text(obs_p, vp, str(p), ha='center', va='bottom',
						zorder=1)

		# next color
		c+=1

	smallest_x = numpy.min([obs_quantiles[0], ens_quantiles[0]])
	largest_x = numpy.max([obs_quantiles[-1], ens_quantiles[-1]])

	# 1:1 line - lowest z order
	sp.plot([smallest_x, largest_x], [smallest_x, largest_x], 'k', lw=2.0,
            zorder=0)
	# limits
	sp.set_xlim([smallest_x, largest_x])
	sp.set_ylim([smallest_x, largest_x])
	sp.set_aspect(1.0)
	return sp, legend_lines
