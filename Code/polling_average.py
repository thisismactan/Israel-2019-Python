exec(open('Code/library.py').read())

## Read data
poll_data = pd.ExcelFile('Data/polls.xlsx')
polls_2009 = pd.read_excel(poll_data, '2009')
polls_2013 = pd.read_excel(poll_data, '2013')
polls_2015 = pd.read_excel(poll_data, '2015')

results = pd.read_excel(poll_data, 'Results')

#### 2019 polling average ####
election_date = dt.date(2019, 4, 9)

## Generate age and weight variables
polls_2019 = (pd.read_excel(poll_data, '2019', usecols = range(16), parse_dates = [0])
                .assign(age = lambda x: (dt.date.today() - x.date).dt.days + 2)
                .assign(weight = lambda x: ((x.date >= dt.date(2019, 2, 21)) & (x.age < 45)) / np.exp(x.age ** 0.4))
                .loc[:,['date', 'age', 'pollster', 'weight', 'taal_hadash', 'balad_raam',
                         'meretz', 'labor', 'blue_white', 'kulanu', 'gesher', 'likud',
                         'yisrael_beiteinu', 'shas', 'utj', 'zehut', 'new_right', 'urwp']]
                )

## Melt
polls_2019_long = (pd.melt(polls_2019, id_vars = ['date', 'pollster', 'age', 'weight'],
                          var_name = 'party', value_name = 'seats')
                    .dropna())
                    
## Convert to logit scale
polls_2019_logit = (polls_2019_long[polls_2019_long.weight != 0]
                    .assign(vote_share = lambda x: np.maximum(0.025, x.seats/120))
                    .assign(vote_logit = lambda x: logit(x.vote_share))
                    )

## Weighted average on logit scale
poll_average_logit = (polls_2019_logit
                      .join(
                              (polls_2019_logit
                               .groupby('party', group_keys = False)
                               .apply(lambda x: np.average(x.vote_logit, weights = x.weight))
                               .rename('mean_vote_logit')
                               ), on = 'party')
                      .loc[:,['date', 'pollster', 'age', 'weight', 'party', 'seats', 
                      'vote_share', 'vote_logit', 'mean_vote_logit']]
                      .assign(dev_sq = lambda x: (x.vote_logit - x.mean_vote_logit) ** 2)
                      )

## Weighted standard errors
poll_stds = (poll_average_logit
             .groupby('party')
             .agg({'dev_sq': ['sum','count'],
                   'weight': 'sum'}
                    )
             .assign(variance = lambda x: x.dev_sq['sum'] / ((x.dev_sq['count'] - 1) * x.weight['sum']))
             .assign(sd = lambda x: x.variance ** 0.5)
             .reset_index()
             .loc[:,['sd']]
             )
             
poll_average_logit = (pd.concat([poll_average_logit
                                .groupby('party')
                                .mean()
                                .reset_index()
                                .loc[:,['party', 'mean_vote_logit']],
                                poll_stds.sd], axis = 1)
                      )

## Compute confidence intervals and convert back to seats
projected_seats = (poll_average_logit
                   .assign(lower_logit = lambda x: x.mean_vote_logit - 1.645*x.sd,
                           upper_logit = lambda x: x.mean_vote_logit + 1.645*x.sd)
                   .assign(lower = lambda x: invlogit(x.lower_logit),
                           seats = lambda x: invlogit(x.mean_vote_logit),
                           upper = lambda x: invlogit(x.upper_logit))
                   .loc[:,['party', 'seats', 'lower', 'upper']])
                   
projected_seats[['lower', 'seats', 'upper']] = (projected_seats[['lower', 'seats', 'upper']]
                                                .apply(lambda x: x - x*(x < 0.0325))
                                                .apply(lambda x: 120*x))

## Plotting the current polling average
ggplot.ggplot(aesthetics = aes(x = 'party', y = 'seats', fill = 'party'), 
              data = projected_seats) +\
              ggplot.geom_bar(stat = 'identity')
