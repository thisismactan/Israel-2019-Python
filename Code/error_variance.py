## Calculates polling error (co)variance by party
exec(open('Code/historical_accuracy.py').read())
exec(open('Code/polling_average.py').read())

## Compute variances on logit scale
poll_error_variance = (pd.concat([error_2009, error_2013, error_2015])
                        .assign(weight = lambda x: 1/(2019 - x.year))
                        .assign(dev_sq = lambda x: (x.error ** 2) * x.weight)
                        .groupby('party')
                        .agg({'dev_sq':'sum',
                              'weight':'sum',
                              'error':'count'})
                        .reset_index()
                        .assign(error_variance = lambda x: (x.dev_sq*x.error)/(x.weight*(x.error - 1)))
                        .loc[:,['party', 'error_variance']])

## Merge onto poll average
poll_averages_logit = (poll_average_logit
                       .merge(poll_error_variance, on = 'party', how = 'left')
                       .iloc[[9, 0, 6, 4, 1, 3, 2, 5, 12, 8, 11, 13, 7, 10],:])

## Easier to add error variance for missing parties by hand...
poll_averages_logit.error_variance[0] = np.mean(poll_error_variance.error_variance[[0, 3]])
poll_averages_logit.error_variance[1] = poll_error_variance.error_variance[13]
poll_averages_logit.error_variance[2] = 0
poll_averages_logit.error_variance[7] = np.mean(poll_error_variance.error_variance[[7, 8, 10]])
poll_averages_logit.error_variance[9] = np.mean(poll_error_variance.error_variance[[0, 3]])
poll_averages_logit.error_variance[10] = poll_error_variance.error_variance[2]
poll_averages_logit.error_variance[13] = poll_error_variance.error_variance[10]

## Compute covariance matrix; assume independence of error variance and sampling variance 
means = poll_averages_logit.mean_vote_logit
variances = np.diag(poll_averages_logit.error_variance)

polls_2019_wide = (polls_2019
                   .loc[:,['taal_hadash', 'balad_raam', 'meretz', 'labor', 'blue_white', 
                           'kulanu', 'gesher', 'likud', 'yisrael_beiteinu', 'shas', 'utj', 
                           'zehut', 'new_right', 'urwp']]
                   .dropna()
                   .apply(lambda x: x/120)
                   .apply(lambda x: np.maximum(0.025, x))
                   .apply(lambda x: logit(x)))

party_covariance = np.cov(polls_2019_wide.values.transpose()) + variances