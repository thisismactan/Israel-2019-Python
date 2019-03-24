## Calculates polling error (co)variance by party
exec(open('Code/historical_accuracy.py').read())
exec(open('Code/polling_average.py').read())

## Compute variances on logit scale
poll_errors_grouped = (pd.concat([error_2009, error_2013, error_2015])
                        .assign(weight = lambda x: 1/(2019 - x.year))
                        .groupby('party')
                        )

poll_errors = (pd.concat([error_2009, error_2013, error_2015])
                .assign(weight = lambda x: 1/(2019 - x.year))
                .groupby('party')
                )