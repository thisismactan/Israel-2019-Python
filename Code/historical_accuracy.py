## Computes historical accuracy of polling in 2009, 2013, and 2015
exec(open('Code/library.py').read())

poll_data = pd.ExcelFile('Data/polls.xlsx')
results = pd.read_excel(poll_data, 'Results')

#### 2009 ####
polls_2009 = pd.read_excel(poll_data, '2009', parse_dates = [0])
results_2009 = results[results['date'].dt.year == 2009]

## Convert to vote shares
polls_2009_vote = pd.concat([polls_2009.loc[:,['date', 'pollster']],
                            (polls_2009
                             .iloc[:,range(2,12)]
                             .apply(lambda x: x/120))], 
                             axis = 1)
                            
## Convert to logit scale
polls_2009_logit = pd.concat([polls_2009.loc[:,['date', 'pollster']],
                            (polls_2009_vote
                             .iloc[:,range(2,12)]
                             .apply(lambda x: logit(x)))], 
                             axis = 1)
                            
## Compute error on logit scale
error_2009 = (pd.melt(polls_2009_logit
              .assign(kadima = lambda x: x.kadima - logit(28/120),
                      labor = lambda x: x.labor - logit(13/120),
                      shas = lambda x: x.shas - logit(11/120),
                      likud = lambda x: x.likud - logit(27/120),
                      yisrael_beiteinu = lambda x: x.yisrael_beiteinu - logit(15/120),
                      arab_parties = lambda x: x.arab_parties - logit(11/120),
                      jewish_home = lambda x: x.jewish_home - logit(3/120),
                      national_union = lambda x: x.national_union - logit(4/120),
                      utj = lambda x: x.utj - logit(5/120),
                      meretz = lambda x: x.meretz - logit(3/120)),
              id_vars = ['date', 'pollster'], var_name = 'party', 
              value_name = 'error'
              )
              .assign(year = 2009,
                      age = lambda x: (dt.date(2009, 2, 10) - x.date).dt.days)
              .query('(age <= 30) & (error != -Inf)')
              )
              
#### 2013 ####
polls_2013 = pd.read_excel(poll_data, '2013', parse_dates = [0])
results_2013 = results[results['date'].dt.year == 2013]

## Convert to vote shares
polls_2013_vote = pd.concat([polls_2013.loc[:,['date', 'pollster']],
                            (polls_2013
                             .iloc[:,range(2,11)]
                             .apply(lambda x: x/120))], 
                             axis = 1)
                            
## Convert to logit scale
polls_2013_logit = pd.concat([polls_2013.loc[:,['date', 'pollster']],
                            (polls_2013_vote
                             .iloc[:,range(2,11)]
                             .apply(lambda x: logit(x)))], 
                             axis = 1)
                            
## Compute error on logit scale
error_2013 = (pd.melt(polls_2013_logit
              .assign(likud_yb = lambda x: x.likud_yb - logit(31/120),
                      labor = lambda x: x.labor - logit(15/120),
                      shas = lambda x: x.shas - logit(11/120),
                      utj = lambda x: x.utj - logit(7/120),
                      jewish_home = lambda x: x.jewish_home - logit(12/120),
                      arab_parties = lambda x: x.arab_parties - logit(11/120),
                      meretz = lambda x: x.meretz - logit(6/120),
                      yesh_atid = lambda x: x.yesh_atid - logit(19/120),
                      hatnuah = lambda x: x.hatnuah - logit(6/120)),
              id_vars = ['date', 'pollster'], var_name = 'party', 
              value_name = 'error'
              )
              .assign(year = 2013,
                      age = lambda x: (dt.date(2013, 1, 22) - x.date).dt.days)
              .query('(age <= 30) & (error != -Inf)')
              )

#### 2015 ####
polls_2015 = pd.read_excel(poll_data, '2015', parse_dates = [0])
results_2015 = results[results['date'].dt.year == 2015]

## Convert to vote shares
polls_2015_vote = pd.concat([polls_2015.loc[:,['date', 'pollster']],
                            (polls_2015
                             .iloc[:,range(2,12)]
                             .apply(lambda x: x/120))], 
                             axis = 1)
                            
## Convert to logit scale
polls_2015_logit = pd.concat([polls_2015.loc[:,['date', 'pollster']],
                            (polls_2015_vote.
                             iloc[:,range(2,12)].
                             apply(lambda x: logit(x)))], 
                             axis = 1)
                            
## Compute error on logit scale
error_2015 = (pd.melt(polls_2015_logit
              .assign(likud = lambda x: x.likud - logit(30/120),
                      yisrael_beiteinu = lambda x: x.yisrael_beiteinu - logit(6/120),
                      yesh_atid = lambda x: x.yesh_atid - logit(11/120),
                      zionist_union = lambda x: x.zionist_union - logit(24/120),
                      jewish_home = lambda x: x.jewish_home - logit(8/120),
                      shas = lambda x: x.shas - logit(7/120),
                      utj = lambda x: x.utj - logit(6/120),
                      meretz = lambda x: x.meretz - logit(5/120),
                      joint_list = lambda x: x.joint_list - logit(13/120),
                      kulanu = lambda x: x.kulanu - logit(10/120)),
              id_vars = ['date', 'pollster'], var_name = 'party', 
              value_name = 'error'
              )
              .assign(year = 2015,
                      age = lambda x: (dt.date(2015, 3, 17) - x.date).dt.days)
              .query('(age <= 30) & (error != -Inf)')
              )
