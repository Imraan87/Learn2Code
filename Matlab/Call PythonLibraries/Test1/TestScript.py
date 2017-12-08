from people import Customer

from logplot import LogPlot
from diagnostics import Diagnostics

C = Customer('Self', 1)

diagnostics = Diagnostics()
results = diagnostics.from_file('C:\\Users\\Imraan\\PycharmProjects\\crossLang\\corellian_74G.log')
LogPlot().plot(results, './results')




A = Customer('Imraan', 30)

C.deposit(50)



