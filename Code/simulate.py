## Simulation
exec(open('Code/error_variance.py').read())

## Seed it
np.random.seed(2019)

## Multivariate normal simulation on logit scale
simulations_logit = np.random.multivariate_normal(mean = means, cov = party_covariance,
                                                  size = 100000)

## Do a series of conversions to calculate corresponding seat counts
simulations_vote = invlogit(simulations_logit)
rowsums = np.sum(simulations_vote, axis = 1)
simulations_vote_scaled = (simulations_vote.transpose() / rowsums).transpose()
simulations_threshold = simulations_vote_scaled >= 0.0325
simulations_vote_thresholded = np.multiply(simulations_vote_scaled, simulations_threshold)
rowsums_thresholded = np.sum(simulations_vote_thresholded, axis = 1)

simulations_vote_final = ((simulations_vote_thresholded.transpose() / rowsums_thresholded)
                            .transpose())
simulations_seats = np.round(simulations_vote_final*120)

## Convert to a data frame
parties = ['taal_hadash', 'balad_raam', 'meretz', 'labor', 'blue_white', 'kulanu',
           'gesher', 'likud', 'yisrael_beiteinu', 'shas', 'utj', 'zehut',
           'new_right', 'urwp']
simulations_df = (pd.DataFrame(simulations_seats, columns = parties)
                    .assign(left = lambda x: x.meretz + x.labor,
                            center = lambda x: x.blue_white,
                            center_right = lambda x: x.kulanu + x.gesher,
                            right = lambda x: x.likud + x.yisrael_beiteinu + x.new_right +
                            x.urwp + x.zehut,
                            arab = lambda x: x.taal_hadash + x.balad_raam,
                            ultraorthodox = lambda x: x.shas + x.utj))

party_seats = (simulations_df.loc[:, parties])
ideology_seats = (simulations_df.loc[:,['left', 'center', 'center_right', 'right', 
                                        'arab', 'ultraorthodox']])

## Which party is largest
(party_seats
 .assign(likud_largest = lambda x: x.likud > x.blue_white,
         blue_white_largest = lambda x: x.blue_white > x.likud,
         both_largest = lambda x: x.blue_white == x.likud)
 .loc[:,['likud_largest', 'blue_white_largest', 'both_largest']]
 .melt(var_name = 'party', value_name = 'prob')
 .groupby('party')
 .agg('mean')
 )

## Breakdown by party
(party_seats
 .melt(var_name = 'party', value_name = 'seats')
 .groupby('party')
 .agg(['mean', pctile(5), pctile(25), pctile(50), pctile(75), pctile(95)])
 .iloc[[9, 0, 6, 4, 1, 3, 2, 5, 12, 8, 11, 13, 7, 10],:])