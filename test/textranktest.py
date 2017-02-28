# coding=utf-8
from textrank import extractKeyphrases,extractSentences
if __name__ == '__main__':
    senten = "SINGAPORE — Certificate of Entitlement (COE) premiums for " \
             "small cars hit a four-month high yesterday, as demand for " \
             "them rose because bigger ones were subject to new taxes " \
             "and car rental firms are buying vehicles in response to " \
             "the growing popularity of car leasing. COE premiums for small " \
             "cars rose to S$73,100 from the previous S$69," \
             "903 to reach the highest level since March. " \
             "Under the Carbon Emissions-Based Vehicle Scheme, " \
             "cars with high carbon emissions equal to or more than 211g CO2km " \
             "will incur a registration surcharge of between " \
             "S$5,000 and S$20,000.Mr Raymond Tang, Honorary Secretary of the " \
             "Singapore Vehicle Traders Association, noted that a surcharge " \
             "would be imposed on a majority of cars in Category B " \
             "(1,601 cc and above) and buyers would instead turn to " \
             "buying luxury makes in Category A (1,600cc and below). " \
             "Adding that there was a “mismatch” in demand and supply of COEs, " \
             "CarTimes Managing Director Eddie Loo said its car-leasing business had doubled. " \
             "He said: “Continental cars are going for 0 per cent down " \
             "payments with the option to buy back, and this has created " \
             "a lot of demand for the leasing option.” While car dealers " \
             "expect a marginal increase in the COE quota for the next six months — " \
             "deregistration numbers for the first " \
             "five months of this year have been higher than that of the corresponding " \
             "period last year — they felt the premiums will continue to head north. " \
             "Mr Loo reiterated there was “no quick fix” to bring down COE prices \"as long as there is a scarcity in supply\". " \
             "Nevertheless, he did not expect COE premiums to exceed S$100,000, " \
             "which he felt was the threshold for most buyers. In recent weeks, " \
             "automobile dealers have been enticing buyers with trade-in offers, " \
             "freebies and pledging to hold prices despite fluctuations in the COE premiums. " \
             "One dealer, Wearnes Automobile, even offered a \"buy one, " \
             "get one free deal for a limited period, under which those who bought " \
             "a new Volvo would get another pre-owned car free."

    summary = extractSentences(senten)
    keyword = extractKeyphrases(summary)
    print summary
    print keyword
