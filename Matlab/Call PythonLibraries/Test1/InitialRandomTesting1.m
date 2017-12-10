[version, executable, isloaded] = pyversion;


LogPlot     = py.logplot.LogPlot('./');
diagnostics = py.diagnostics.Diagnostics();
results = diagnostics.from_file('C:\\Users\\Imraan\\PycharmProjects\\crossLang\\corellian_74G.log');
LogPlot.plot(results, './results')


%%
C = py.people.Customer('Python',30)
C2 = Customer('Matlab',677)
LogPlot = py.logplot.LogPlot('./')


diagnostics = py.diagnostics.Diagnostics()
results = diagnostics.from_file('C:\\Users\\Imraan\\PycharmProjects\\crossLang\\corellian_74G.log')

LogPlot.dac_initialisation(results{'DACQ'}, 'DACQ', '.\')


C.deposit(50)