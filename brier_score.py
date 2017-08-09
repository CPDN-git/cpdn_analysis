###############################################################################
# File         : brier_score.py
# Author       : Neil Massey
# Created      : 14/06/11
# Purpose      : Calculate Brier Score
###############################################################################

import numpy
from calc_dichot_event_bins import calc_dichot_event_bins

###############################################################################

def brier_score(obs, forc, thresh_fn, obs_thresh_val, forc_thresh_val=None):
	# calculate the Brier Score from the observations:

	# Simple (non decomposed) Brier Score is \frac{1}{K}\sum_{k=1}^K(r_k - d_k)^2
	# where r_k = probability of event occurring on kth occasion in the forecast
	#       d_k = 1 if event occurred on kth occasion in obs, 0 if not occurred

	# inputs
	# obs        : vector of observed values
	# forc       : matrix of forecasts [n,m] where n is number of ensemble members, 
	#              m is same length as obs
	# thresh_fn  : thresholding function - return indices that pass function
	# thresh_val : value to use in thresholding function

	# determine which indices in the observed values meet the threshold and set to 1
	obs_binary = numpy.zeros(obs.shape)
	obs_thresh_idx = thresh_fn(obs, obs_thresh_val)
	obs_binary[obs_thresh_idx] = 1
	# do the same for the forecast
	if forc_thresh_val == None:
		forc_thresh_val = obs_thresh_val
	forc_binary = numpy.zeros(forc.shape)
	forc_thresh_idx = thresh_fn(forc, forc_thresh_val)
	forc_binary[forc_thresh_idx] = 1
	# condense forecast to probabilities
	forc_probs = numpy.sum(forc_binary, axis=0)
	forc_probs = forc_probs / forc_probs.shape[0]
	# calc the Brier Score
	bs = numpy.sum(numpy.square(forc_probs - obs_binary)) / obs_binary.shape[0]
	return bs

###############################################################################

def brier_score_2(obs, forc, thresh_fn, obs_thresh_val, forc_thresh_val=None, bw=0.1):
	prob_bins, obs_freq, bin_count = calc_dichot_event_bins(obs, forc, thresh_fn, 
										obs_thresh_val, forc_thresh_val, bw)
	K = obs.shape[0]
	sum = numpy.sum(numpy.square(prob_bins - obs_freq))
	bs = sum / K
	return bs

###############################################################################

def brier_score_dc(obs, forc, thresh_fn, obs_thresh_val, forc_thresh_val=None, bw=0.1):
	# calculate the decomposed Brier Score into reliability, resolution and
	# variance

	# inputs
	# obs        : vector of observed values
	# forc       : matrix of forecasts [n,m] where n is number of ensemble members, 
	#              m is same length as obs
	# thresh_fn  : thresholding function - return indices that pass function
	# thresh_val : value to use in thresholding function
	# bw         : (probability) bin width

	# outputs
	# bs, cmpts  : bs = Brier Score, cmpts = tuple of (var, res, rel)

	# get the probability bins, relative observed frequency and forecast count
	# for the bins
	prob_bins, obs_freq, bin_count = calc_dichot_event_bins(obs, forc, thresh_fn, 
										obs_thresh_val, forc_thresh_val, bw)

	# now calculate the constituent parts of the Brier Score
	T = prob_bins.shape[0]			# number of bins
	K = numpy.sum(bin_count)		# number of forecasts
	# calc variance
	d_bar_sum = numpy.sum(bin_count*obs_freq)
	d_bar = d_bar_sum / K
	var = d_bar * (1-d_bar)

	# calc reliability
	rel_sum = numpy.sum(bin_count*(numpy.square(prob_bins-obs_freq)))
	rel = rel_sum / K

	# calc resolution
	res_sum = numpy.sum(bin_count*(numpy.square(obs_freq - d_bar)))
	res = res_sum / K

	# calculate the actual Brier Score
	bs = var + rel - res
	return bs, (var, rel, res)

###############################################################################

def thresh_gt_score(data, score):
	# thresholding function - input is a numpy array
	return numpy.where(data > score)

###############################################################################

def thresh_lt_score(data, score):
	# thresholding function - input is a numpy array
	return numpy.where(data < score)

