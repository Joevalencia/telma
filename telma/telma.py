import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from time import strftime
import requests
import json
import warnings

send_url = "http://ipinfo.io"
geo_req = requests.get(send_url)
geo_json = json.loads(geo_req.text)
warnings.filterwarnings('ignore')
plt.style.use('seaborn-darkgrid')


class BiometricModel:
    """
    This class permits carrying out multliples basic calculation in life actuarial science.

    From the computation of the basic actuarial table to life expectancy estimation based on a given cohort(s) functions.

    """

    def actuarialtable(self, cohort1):
        """

        This function computes the basic actuarial table given a cohort (lx):
        the number of people who survive to age x.

        :param cohort1: array-like. It refers to the l{x} vector.

        :return: This method returns a Pandas DataFrame of 8 columns of the cohorts.
                 These columns are composed by Livings, Deaths, q_{x}, p_{x}, L{x}, m{x}, T{x}, e{x}.

        p{x}: The probability that someone aged exactly x will survive to age (x+1). This is l{x+1}/l{x}.

        q{x}: The probability that someone aged exactly x will die before reaching age (x+1).

        d{x}: The number of people who die aged x last birthday. This is d{x} = l{x} - l{x+1} = l{x}*q{x}.

        L{x}: The average number of living in the interval between the exact ages x and x + n.

        T{x}: The total population aged x and older, or the total number of years people lived since age x.

        m{x}: This symbol refers to central rate of mortality.

        e{x}: Life expectancy at the exact age x. That is the average number of years lived by a person since age x.

        """

        px1 = (cohort1.shift(-1) / cohort1).fillna(0)
        qx1 = 1 - px1
        dx1 = qx1 * cohort1
        l1 = ((cohort1 + cohort1.shift(1)) / 2).shift(-1)
        tx = []
        for i in range(0, len(l1)):
            tx.append(sum(l1[i:-1]))
        mx = dx1 / l1
        e = []
        for i in range(0, len(cohort1[:-1])):
            lex = cohort1[i]
            e.append(sum(cohort1[i + 1:-1]) / lex)
        exs = pd.Series(e)
        at1 = 0
        if int(cohort1[-1:]) != 0:
            at1 = cohort1.index[-1] + 1
        else:
            at1 = cohort1.index[-1]
        df1 = pd.DataFrame({'l(x)': cohort1, 'dx': dx1,
                            'qx': qx1, 'px': px1,
                            'Lx': l1, 'Tx': tx, 'mx': mx,
                            'ex curtate': exs})
        print('--' * 25)
        print(f'Actuarial Table of {cohort1.name}:')
        print('--' * 25)
        print('Date and Time: ', strftime("%a, %d %b %Y %H:%M:%S"))
        print('Region and Country: ', geo_json['region'], ',', geo_json['country'])
        print('Omega \u03C9 : ', at1)
        return df1

    def actuarialtable2(self, cohort1, cohorte2):

        """
        This method return a Pandas DataFrame of 8 columns for each of the two cohorts.
        These columns are composed by Livings, Deaths, q_{x}, p_{x}, L{x}, m{x}, T{x}, e{x}.

        :return: Actuarial Table for 2 lives
        'Note: Either ex, ey refer to curtate life expectancy
         Note: cohort1 referts to l{x} and cohort2 to l{y}.

        p{y}: The probability that someone aged exactly y will survive to age (y+1). This is l{y+1}/l{y}.

        q{y}: The probability that someone aged exactly y will die before reaching age (y+1).

        d{y}: The number of people who die aged y last birthday. This is d{y} = l{y} - l{y+1} = l{y}*q{y}.

        L{y}: The average number of living in the interval between the exact ages y and y + n.

        T{y}: The total population aged y and older, or the total number of years people lived since age y.

        m{y}: This symbol refers to central rate of mortality.

        e{y}: Life expectancy at the exact age y. That is the average number of years lived by a person since age y.

        Same for x.

        """

        ful = []
        if len(cohort1) != len(cohorte2):
            for i in range(abs(len(cohort1) - len(cohorte2))):
                ful.append(0)
            cohort2 = cohorte2.append(pd.Series(ful),
                                      ignore_index=True).astype(str(cohort1.dtype))
        else:
            cohort2 = cohorte2

        px1 = (cohort1.shift(-1) / cohort1).fillna(0)
        px2 = (cohort2.shift(-1) / cohort2).fillna(0)
        qx1, qx2 = 1 - px1, 1 - px2
        dx1, dx2 = qx1 * cohort1, qx2 * cohort2
        l1 = ((cohort1 + cohort1.shift(1)) / 2).shift(-1)
        tx1 = []
        for i in range(0, len(l1)):
            tx1.append(sum(l1[i:-1]))
        mx1 = dx1 / l1
        e1 = []
        for i in range(0, len(cohort1[:-1])):
            lex = cohort1[i]
            e1.append(sum(cohort1[i + 1:-1]) / lex)
        exs = pd.Series(e1).fillna(0)

        l2 = ((cohort2 + cohort2.shift(1)) / 2).shift(-1)
        tx2 = []
        for i in range(0, len(l2)):
            tx2.append(sum(l2[i:-1]))
        mx2 = dx2 / l2
        e2 = []
        for i in range(0, len(cohort2[:-1])):
            ley = cohort2[i]
            e2.append(sum(cohort2[i + 1:-1]) / ley)
        eys = pd.Series(e2).fillna(0)
        at1, at2 = 0, 0
        if int(cohort1[-1:]) != 0 and int(cohorte2[-1:]) != 0:
            at1 = cohort1.index[-1] + 1
            at2 = cohorte2.index[-1] + 1
        elif int(cohort1[-1:]) != 0:
            at1 = cohort1.index[-1] + 1
            at2 = cohorte2.index[-1]
        elif int(cohorte2[-1:]) != 0:
            at1 = cohort1.index[-1]
            at2 = cohorte2.index[-1] + 1
        elif int(cohort1[-1:]) == 0 and int(cohorte2[-1:]) == 0:
            at1 = cohort1.index[-1]
            at2 = cohorte2.index[-1]

        df1 = pd.DataFrame({'l(x)': cohort1,
                            'l(y)': cohort2,
                            'dx': dx1, 'dy': dx2,
                            'qx': qx1, 'qy': qx2,
                            'px': px1, 'py': px2,
                            'Lx': l1, 'Ly': l2,
                            'Tx': tx1, 'Ty': tx2,
                            'mx': mx1, 'my': mx2,
                            'ex': exs, 'ey': eys})
        print('--' * 35)
        print(f'Actuarial Table of {cohort1.name} and {cohorte2.name}:')
        print('--' * 35)
        print('Date and Time: ', strftime("%a, %d %b %Y %H:%M:%S"))
        print('Region and Country:', geo_json['region'], ',', geo_json['country'])
        print('Omega 1 \u03C9 : ', at1)
        print('Omega 2 \u03C9 : ', at2)
        return df1

    def omega(self, cohort1, cohort2=None):
        """
        Older age of the cohort. This value is known as Actuarial Infinity
        and it is denotes with omega: \u03C9

        :param cohort2: Array-like The cohort function (lx).

        :param cohort1: Array-like The cohort function (lx).

        :return: Last age of the cohort. It is assumed that the index is age-based.
        """

        omega1, omega2 = 0, 0
        if int(cohort1[-1:]) != 0:
            omega1 = cohort1.index[-1] + 1
        else:
            omega1 = cohort1.index[-1]
        if cohort2 is not None:
            if int(cohort1[-1:]) != 0:
                omega1 = cohort1.index[-1] + 1
            else:
                omega1 = cohort1.index[-1]
            if int(cohort2[-1:]) != 0:
                omega2 = cohort2.index[-1] + 1
            else:
                omega2 = cohort2.index[-1]
            return omega1, omega2
        return omega1

    def Lx(self, cohort, age: int):
        """
        Census survival Function (Lx). It is number of years of life lived between ages x and (x+1) of those currently aged x.

        :param cohort: The cohort function (lx).

        :param age: The age of the individual.

        :return: L{x}: The average number of living in the interval between the exact ages x and x + n.
        """
        c1 = ((cohort / cohort.shift(1)).shift(-1)).fillna(0)
        dx = (1 - c1) * cohort
        Lx = cohort[age] - dx[age] / 2

        return Lx

    def Tx(self, cohort, age: int):
        """
         T{x}: The total population aged x and older, or the total number of years people lived since age x.

        :param cohort: The cohort function (lx).

        :param age: The age of the individual.

        :return: Tx at the age x.
        """
        l1 = ((cohort + cohort.shift(1)) / 2).shift(-1)
        tx = []
        for i in range(0, len(l1)):
            tx.append(sum(l1[i:-1]))

        return tx[age]

    def central_rate_mortality(self, cohort, age: int):
        """
        The central death rate. Is defined as mx=dx/Lx.

        :param cohort: The cohort function (lx).

        :param age: The age of the individual.

        :return: The central death rate at age x.
        """
        c1 = (cohort.shift(-1) / cohort).fillna(0)
        dx = (1 - c1) * cohort  # Tanto central de mortalidad anual
        Lx = cohort - dx / 2
        mx = dx[age] / Lx[age]
        return round(mx, 7)

    def life_expectancy(self, cohort, age=0, kind: str = 'complete'):  # exn
        """
        This function computes the life expectancy at ages x.

        :param cohort:  The cohort function (lx).

        :param age:  The age of the individual.

        :param kind:  Type of life expectancy calculated. "Complete" or "curtate" can be computed.

        :return: The life expectancy of the individual aged x.

        """

        t = pd.Series(np.arange(1, (120 - age + 1)))
        c1 = (cohort[age + t].sum()) / cohort[age]
        if kind == 'complete':
            return c1.round(2) + .5
        elif kind == 'curtate':
            return c1.round(2)
        else:
            print('Error. Kind parameter only accepts "complete" or "curtate"')


class OneLife:
    """

    This class refers to life actuarial basic calculation on one individual based on a given cohort (lx).

    The life plot permits charting the cohort function in a static or dinamic mode either. (Plotly is required)

    """

    def lifeplot(self, cohort1, interactive: bool = False,
                 death: bool = False, qx_log: bool = False):
        """
        It plots the graph of the cohort interactively or static either.
        By default is static and plots dx chart.

        :param qx_log: If True it display the log(qx) interactively.

        :param death:  If True it display the deaths interactively.

        :param cohort1: Array-like Cohort function (lx).

        :param interactive: Bool: It displays an interactive chart of
                the survival plot using Plotly.

        :return: Survival Plot of two cohort.
        """

        px1 = ((cohort1 / cohort1.shift(1)).shift(-1)).fillna(0)
        qx1 = 1 - px1
        dx1 = qx1 * cohort1

        if not interactive:
            plt.figure(figsize=(15, 5))
            p0 = plt.subplot(1, 2, 1)
            plt.title(f'Survival Plot of {cohort1.name}', fontweight='bold')
            plt.xlabel('Age', fontweight='bold')
            plt.ylabel('Living people ($l_{x}$)', fontweight='bold')
            plt.xlim([0, 115])
            plt.plot(cohort1.index, cohort1, label=f'{cohort1.name}', color='red')
            plt.legend()
            p1 = plt.subplot(1, 2, 2)
            plt.title(f'Death Plot of {cohort1.name}', fontweight='bold')
            plt.xlabel('Age', fontweight='bold')
            plt.ylabel('Death people ($d_{x}$)', fontweight='bold')
            plt.xlim([0, 115])
            if qx_log:
                plt.title(f'LogDeath Plot of {cohort1.name}', fontweight='bold')
                plt.plot(np.log(qx1), label=f'{cohort1.name}', color='red')
                plt.legend()
                plt.show()
            else:
                plt.plot(dx1, label=f'{cohort1.name}', color='red')
                plt.legend()
                plt.show()

        else:

            import plotly.graph_objects as go
            import plotly.express as px

            if not death:
                px1 = ((cohort1 / cohort1.shift(1)).shift(-1)).fillna(0)
                qx1 = 1 - px1
                dx1 = qx1 * cohort1
                e = []
                for i in range(0, len(cohort1[:-1])):
                    lex = cohort1[i]
                    e.append(sum(cohort1[i + 1:-1]) / lex)
                exs = pd.Series(e)

                df1 = pd.DataFrame({'l(x)': cohort1, 'Life expectancy': round(exs, 2),
                                    'Age': cohort1.index})

                fig = px.line(df1, x='Age', y='l(x)', hover_name='Life expectancy',
                              title=f'Survival plot of {cohort1.name}')
                fig.update_traces(line=dict(color="crimson", width=2))
                fig.update_layout(
                    font_family="COLLEGE",
                    font_color="blue",
                    title_font_family="New Times Rowan",
                    title_font_color="red",
                    legend_title_font_color="green")

                fig.show()

            else:

                plot1 = go.Scatter(x=cohort1.index, y=qx1, mode='lines',
                                   name=f'Plot of log q_x - {cohort1.name}')
                figure = go.Figure([plot1])
                figure.update_layout(title_text=f'Death Plot of {cohort1.name}',
                                     xaxis_title='Age',
                                     yaxis_title='Death of people $d_{x}$',
                                     font_family='COLLEGE', font_color='black',
                                     title_font_color='red', title_font_family='New Times Rowan',
                                     legend_title_font_color='green')

                figure.show()

    def d_x(self, cohort, age: int, t: int = 1):
        """
        This function computes the numbers of the between x and x+1.

        :param cohort: Array-like. The cohort function (lx).

        :param age: Int. The age of the individual.

        :param t: Int. The age from which start differencing.

        :return: The numbers of death within x and x+t.

        """

        temporal = t
        sum2 = age + temporal
        dif1 = cohort[age] - cohort[sum2]
        print(f'The number of deaths between {age} and {temporal} are:')
        return dif1

    def p_x(self, cohort, age: int, t: int = 1,
            i: float = .02, capital: float = 1,
            lump_sum: bool = False):
        """
        p_x is the probability that (x) survives to at least age x + t.

        :param i: Float : It is the interest rate.

        :param capital: Float : It is the amount the insurer would paid.

        :param lump_sum: Boolean : If True it computes life insurance lump_sum.

        :param cohort: Array-like : It refers to the living's vector.

        :param age: Int : It refers to the actual age of the individual.

        :param t: Int : It refers to the time ahead. By default 1.

        :return: The Probability that (x) survives to at least age x + t.

        """

        temporal = t
        factor = (1 + i) ** (-temporal)
        s = age + temporal
        probability = np.roll(cohort[s], 1) / cohort[age]
        value = round(factor * probability * capital, 2)
        if not lump_sum:
            print(f'The probability that {age} will survive within {temporal} is:')
            return probability
        else:
            print('The life insurance to pay is:')
            return value, (probability * factor)

    def q_x(self, cohort, age: int, t: int = 1):
        """
           q_{x} is the probability that (x) dies before age x + t.

        :param cohort: Array-like : It refers to the living poeple's vector.

        :param age: Int : It refers to the actual age of the individual.

        :param t: Int : It refers to the period ahead. By default 1.

        :return: The probability that (x) dies before age x + t.

        """

        temporal = t
        a = age + temporal
        deaths = np.roll(cohort[age], 1) - cohort[a]
        probability = deaths / cohort[age]
        print(f'The probability that {age} will die within {temporal} is:')
        return probability

    def deferred_mqx(self, cohort, age: int, m: int = 1,
                     n: int = 1):
        """
        - The probability that a person aged exactly x dies between exact ages (x+n) and (x+m+n).

        :param cohort: The cohort function (lx).

        :param age:  The age of the individual.

        :param m:  Int. The deferred period. The period m is sometimes referred to as the deferred period.

        :param n: Period until which the age should be evaluated

        :return:

        """

        temporal, survival = n, m
        sum1 = age + temporal
        sum2 = age + temporal + survival
        death = cohort[sum1] - cohort[sum2]
        probability = death / cohort[age]
        print(f'The probability that {age} will survive within {temporal} is:')
        return probability


class MultipleLives:
    """
        This class refers to life actuarial basic calculation on one individual based on a given cohort (lx).

        The life plot permits charting the cohort function in a static or dinamic mode either. (Plotly is required)
        Furthemore is strongly advided inserting in "cohorte2" the cohort function that has a different length from
        "cohort1" and "model".

        See example in Jupyter examples.

        """

    def lifeplot_2(self, cohort1, cohorte2, model=None, interactive: bool = False, qx_log: bool = False,
                   death: bool = False):

        """
        It plots the graph of multiple cohorts interactively or static either.

        :param cohort1: The cohort function (lx).

        :param cohorte2: The cohort function (ly).
                         If len(ly)<len(x) please consider passing ly as cohorte.

        :param model: A third cohort function (lz).

        :param qx_log: If True it displays log(qx) cohorts using plotly.

        :param interactive: If True it displays cohorts interactively using plotly.

        :param death: If True it displays dx cohorts using plotly.

        :return: Living Plot, Log(qx) or dx either.

        """

        ful = []  ## considerar poner como cohorte2 el vector que tiene diferente longitud en interactively
        if len(cohort1) != len(cohorte2):
            for i in range(abs(len(cohort1) - len(cohorte2))):
                ful.append(0)
            cohort2 = cohorte2.append(pd.Series(ful),
                                      ignore_index=True).astype(str(cohort1.dtype))

        else:
            cohort2 = cohorte2

        #
        px1 = (cohort1.shift(-1) / cohort1).fillna(0)
        px2 = (cohort2.shift(-1) / cohort2).fillna(0)
        qx1, qx2 = 1 - px1, 1 - px2
        dx1, dx2 = qx1 * cohort1, qx2 * cohort2
        qx22 = 1 - (cohorte2.shift(-1) / cohorte2).fillna(0)
        dx22 = qx22 * cohorte2

        e1 = []
        for i in range(0, len(cohort1[:-1])):
            ley = cohort1[i]
            e1.append(sum(cohort1[i + 1:-1]) / ley)
        eyx = pd.Series(e1) + .5

        e2 = []
        for i in range(0, len(cohort2[:-1])):
            ley = cohort2[i]
            e2.append(sum(cohort2[i + 1:-1]) / ley)
        eys = pd.Series(e2) + .5

        df1 = pd.DataFrame({f'{cohort1.name}': cohort1, 'e\u20931': round(eyx, 2),
                            f'{cohort2.name}': cohort2, 'e\u20932': round(eys, 2),
                            'Age': cohort1.index, f'Death {cohort1.name}': dx1,
                            f'Death {cohort2.name}': dx2})

        if not interactive:
            plt.figure(figsize=(15, 5))
            p0 = plt.subplot(1, 2, 1)
            plt.title(f'Survival Plot of {cohort1.name} '
                      f'and {cohorte2.name}', fontweight='bold')
            plt.xlabel('Age', fontweight='bold')
            plt.ylabel('Living people ($l_{x}$) and ($l_{y}$)', fontweight='bold')
            plt.xlim([0, 120])
            plt.plot(cohort1.index, cohort1, label=f'{cohort1.name}', color='darkorange')
            plt.plot(cohorte2.index, cohorte2, label=f'{cohorte2.name}', color='midnightblue')
            # plt.legend()
            if model is not None:
                plt.plot(model.index, model, label=f'{model.name}', color='red')
            plt.legend()
            p1 = plt.subplot(1, 2, 2)
            plt.title(f'Death Plot of {cohort1.name} '
                      f'and {cohorte2.name}', fontweight='bold')
            plt.ylabel('Death people ($d_{x}$) and ($d_{y}$)', fontweight='bold')
            plt.xlabel('Age', fontweight='bold')
            plt.xlim([0, 120])
            if qx_log is True:
                plt.title(f'LogDeath Plot of {cohort1.name} '
                          f'and {cohorte2.name}', fontweight='bold')
                plt.ylabel('LogDeath ($d_{x}$) and ($d_{y}$)', fontweight='bold')
                plt.plot(np.log(qx1), label=f'{cohort1.name}', color='darkorange')
                plt.plot(np.log(qx22), label=f'{cohorte2.name}', color='midnightblue')
            else:
                plt.plot(dx1, label=f'{cohort1.name}', color='darkorange')
                plt.plot(dx22, label=f'{cohorte2.name}', color='midnightblue')

            if model is not None:
                pxm = ((model / model.shift(1)).shift(-1)).fillna(0)
                qxm = 1 - pxm
                dxm = qxm * model

                if qx_log is True:
                    plt.plot(np.log(qxm.replace(0, 1)), label=f'{model.name}', color='red')
                else:
                    plt.plot(dxm, label=f'{model.name}', color='red')

            plt.legend()

            plt.show()

        else:
            import plotly.express as px
            if not death:
                fig = px.line(df1, x='Age', y=[f'{cohort1.name}', f'{cohort2.name}'],
                              hover_data=['e\u20931', 'e\u20932'],
                              title=f'Survival plot of {cohort1.name} and {cohort2.name}')
            else:
                if qx_log is True:
                    fig = px.line(df1, x='Age', y=[f'Death {cohort1.name}', f'Death {cohort2.name}'],
                                  hover_data=['e\u20931', 'e\u20932'], log_y=True,
                                  title=f'LogDeath plot of {cohort1.name} and {cohort2.name}')
                else:
                    fig = px.line(df1, x='Age', y=[f'Death {cohort1.name}', f'Death {cohort2.name}'],
                                  hover_data=['e\u20931', 'e\u20932'],
                                  title=f'Death plot of {cohort1.name} and {cohort2.name}')
            if model is not None:
                pxm = ((model / model.shift(1)).shift(-1)).fillna(0)
                qxm = 1 - pxm
                dxm = qxm * model
                em = []
                for s in range(0, len(model[:-1])):
                    luc = model[s]
                    em.append(sum(model[s + 1:-1]) / luc)
                emm = pd.Series(em) + .5
                df2 = pd.DataFrame({f'{cohort1.name}': cohort1, f'qx_{cohort1.name}': round(qx1, 7),
                                    f'{cohort2.name}': cohort2, f'qx_{cohort2.name}': round(qx2, 7),
                                    f'{model.name}': model, f'qx_{model.name}': round(qxm, 7),
                                    'Age': cohort1.index, f'Death {cohort1.name}': round(dx1, 2),
                                    f'Death {cohort2.name}': round(dx2, 2), f'Death {model.name}': round(dxm, 2),
                                    'e\u20931': round(eyx, 2), 'e\u20932': round(eys, 2),
                                    'e\u20933': round(emm, 2)})
                if death is True:

                    fig = px.line(df2, x='Age', y=[f'Death {cohort1.name}',
                                                   f'Death {cohort2.name}',
                                                   f'Death {model.name}'],
                                  hover_data=[f'qx_{cohort1.name}', f'qx_{cohort2.name}', f'qx_{model.name}'],
                                  title=f'Death plot of {cohort1.name}, {cohort2.name} and {model.name}')
                    if qx_log is True:
                        fig = px.line(df2, x='Age', y=[f'qx_{cohort1.name}',
                                                       f'qx_{cohort2.name}',
                                                       f'qx_{model.name}'], log_y=True,
                                      hover_data=[f'Death {cohort1.name}',
                                                  f'Death {cohort2.name}',
                                                  f'Death {model.name}'],
                                      title=f'Log_qx plot of {cohort1.name}, {cohort2.name} and {model.name}')

                else:
                    fig = px.line(df2, x='Age', y=[f'{cohort1.name}',
                                                   f'{cohort2.name}',
                                                   f'{model.name}'],
                                  hover_data=['e\u20931', 'e\u20932', 'e\u20933'],
                                  title=f'Survival plot of {cohort1.name}, {cohorte2.name} and {model.name}')
            fig.show()

    def p_xy(self, c1, c2, age_x: int, age_y: int, m=0,
             t: int = 1):
        """
        The probability that x and y will survive t years.

        :param m: The deferred period.

        :param c1: The cohort function l(x).

        :param c2: cohort function l(y).

        :param age_x: The age of x.

        :param age_y: The age of y.

        :param t: Period until which the age should be evaluated.

        :return: The probability that x and y will survive t years.

        """

        temporal = t
        sumx = age_x + temporal + m
        sumy = age_y + temporal + m
        probabilityx = np.roll(c1[sumx], 1) / c1[age_x]
        probabilityy = np.roll(c2[sumy], 1) / c2[age_y]
        probability = probabilityx * probabilityy
        print(f'The probability that both lives {age_x} and {age_y}'
              f' will be alive after {temporal} years is:')
        return probability

    def q_xy(self, c1, c2, age_x: int, age_y: int,
             t: int = 1):
        """
        It is the probability that at least one of lives (x)
        and (y) will be dead within t years.

        :param c1: cohort function lx.

        :param c2: cohort function ly.

        :param age_x: age of x.


        :param age_y: age of y.

        :param t: Period until which the age should be evaluated.

        :return: The probability that at least one of lives (x)
                    and (y) will be dead within t years.

        """
        temporal = t
        sumx = age_x + temporal
        sumy = age_y + temporal
        probabilityx = np.roll(c1[sumx], 1) / c1[age_x]
        probabilityy = np.roll(c2[sumy], 1) / c2[age_y]
        probability = (1 - probabilityx * probabilityy)
        print(f'The probability that at least one of lives {age_x} and {age_y}'
              f' will be dead within {temporal} years is:')
        return probability

    def no_extinction(self, c1, c2, age_x: int, age_y: int,
                      t: int = 1):
        """
        At least one individual will survive within t years

        :param c1: Array-like. Cohort 1.

        :param c2: Array-like. Cohort 2.

        :param age_x: Int. Age of x.

        :param age_y: Int. Age of y.

        :param t: Int. Period until which the age should be evaluate.

        :return: A probability that at least one of x and y will survive.

        """

        temporal = t
        sumx = age_x + temporal
        sumy = age_y + temporal
        probabilityx = np.roll(c1[sumx], 1) / c1[age_x]
        probabilityy = np.roll(c2[sumy], 1) / c2[age_y]
        probability = probabilityx * probabilityy
        value = probabilityy + probabilityx - probability
        print(f'The probability that at least one of lives {age_x} '
              f'and {age_y} will be alive after {temporal} years is:')
        return value

    def dissolution_no_ex(self, c1, c2, age_x: int, age_y: int,
                          t: int = 1):
        """
        The probability that exactly one life will survive(remain) within t years.

        :param c1: Array-like. The Cohort function (lx).

        :param c2: Array-like. The Cohort function l(y).

        :param age_x: Int. Age of one individual from cohort 1.

        :param age_y: Int. Age of one individual from cohort 2.

        :param t: Period until which the age should be evaluated.

        :return: The probability that exactly one individual will survive within t years.

        """

        temporal = t
        sumx = age_x + temporal
        sumy = age_y + temporal
        probabilityx = np.roll(c1[sumx], 1) / c1[age_x]
        probabilityy = np.roll(c2[sumy], 1) / c2[age_y]
        probability = probabilityx * probabilityy
        value = probabilityy + probabilityx - (2 * probability)
        print(f'The probability that exactly one life will survive withing {t} years is: ')
        return value

    def extinction(self, c1, c2, age_x: int, age_y: int,
                   t: int = 1):
        """
        The is the probability that both lives (x) and (y) will be dead within t
        years.

        :param c1: The cohort function lx.

        :param c2: The cohort function ly.

        :param age_x: The age of x.

        :param age_y: The age of y.

        :param t: Period until which the age should  be evaluated.

        :return: The probability that both lives will die within t years.
        """

        temporal = t
        sumx = age_x + temporal
        sumy = age_y + temporal
        probabilityx = np.roll(c1[sumx], 1) / c1[age_x]
        probabilityy = np.roll(c2[sumy], 1) / c2[age_y]
        probability = probabilityx * probabilityy
        v = probabilityy + probabilityx - probability
        value = 1 - v
        print(f'The probability that both lives {age_x} and {age_y}'
              f' will be dead within {temporal} years is: ')
        return value


class SpainOperation:

    """

    This class is particularly focus on SPANISH life actuarial calculation since annuity are calculated using the BOE.

    Esta clase està principalmente dirigida a las operaciones actuariales del estado espanol, desde el momento en
     que para llevar algunos calculo se usan como referencia las indicaciones del BOE y las PASEM/PERM.

    """


    def seguro_fallecimiento(self, tabla_mortalidad):

        """

        Esta funciòn permite calcular un seguro de fallecimiento con misma frecuencia de variaciòn
        de cuantìa y pago. Ademas permite calcular un seguro con frecuencia de varianciòn de
        cuantìa y pago diferente. Notar que el computo requiere como parametro la tablas de mortalidad
        PASEM. Los datos para el càlculo se ingresan como input.

        :param tabla_mortalidad: Tabla de mortalidad NO GENERACIONALES PASEM

        :return: VALOR ACTUAL ACTUARIAL DEL SEGURO DE FALLECIMIENTO

        """

        frac_freq = int(input('Frecuencia deseada de fraccionamiento: '))
        x = int(input('Ingrese la edad del tomador del seguro: '))
        m = int(input('Ingrese el periodo de diferimiento: '))
        n = int(input('Temporalidad deseada: '))
        if n == 109:
            n = 109 - (x + m)
        elif n != 109:
            n = n
        else:
            print('Error! Type a new "n" ')
        taula = int(input('Tabla NO GENERACIONAL a escoger:\n'
                          '1: PASEM M 1° ORDEN\n'
                          '2: PASEM F 1° ORDERN\n'
                          '3: PASEM UNISEX 1° ORDEN\n'
                          '4: PASEM M 2° ORDEN\n'
                          '5: PASEM F 2° ORDEN\n'
                          '6: PASEM UNISEX 2° ORDEN\n'))
        L = tabla_mortalidad.iloc[:, taula]
        fr = np.arange(frac_freq) / frac_freq
        jon = np.outer(L[1:], fr)
        jon1 = np.outer(L[:-1], (1 - fr))
        jj = (jon + jon1).flatten().round(2)  # Tabla creada con fraccionamiento
        interest = float(input('Tasa de interés: '))  # Base técnica de la operaciòn
        t = np.arange((m * frac_freq), ((m + n) * frac_freq))  # t Periodos del sumatorio
        v = (1 + interest) ** -((t + 1) / frac_freq)
        q1 = jj[x * frac_freq + t] - jj[x * frac_freq + t + 1]
        q2 = jj[x * frac_freq]
        q = q1 / q2  # qx fallecimiento pospagable
        a1 = input('Seguro Continuo o Discreto: ').lower()
        capital = input('Ingrese el tipo de Seguro:\n'
                        '"Constante"\n'
                        '"Aritmetica" o "Lineal"\n'
                        '"Geometrica" o "Acumulativa"\n').lower()
        v1 = interest / np.log(1 + interest)  # Tanto para el seguro continuo
        a2 = input('Frecuencia de variaciòn de pago y cuantìa diferentes? ').lower()
        if a2 in 'no':
            if capital == 'constante':
                k1 = int(input('Cuantìa del capital: '))
            elif capital in ('aritmetica', 'lineal'):
                k2 = float(input('Primer termino: '))
                k2_ = float(input('Segundo termino: '))
                k1 = k2 + k2_ * (t - m * frac_freq)
            elif capital in ('geometrica', 'acumulativa'):
                k3 = float(input('Primer termino: '))
                k3_ = float(input('Tanto acumulativo: '))
                k33 = 1 + k3_
                k1 = k3 * k33 ** (t - m * frac_freq)
            else:
                print('Error')
            if a1 in ('continuo', 'no discreto'):
                valor = sum(k1 * q * v) * v1
            elif a1 in ('no continuo', 'discreto'):
                valor = sum(k1 * q * v)
            else:
                print('Error!')
        elif a2 in 'si':
            a3 = int(input('Ingrese la frecuencia de variaciòn de pago (k)\n'
                           'Se refiere al número de términos de igual cuantía dentro de cada período de variación: '))
            if capital == 'constante':
                k1 = int(input('Cuantìa del capital: '))
            elif capital in ('aritmetica', 'lineal'):
                k2 = float(input('Primer termino: '))
                k2_ = float(input('Segundo termino: '))
                k1 = k2 + k2_ * np.floor((t - m * frac_freq) / a3)
            elif capital in ('geometrica', 'acumulativa'):
                k3 = float(input('Primer termino: '))
                k3_ = float(input('Tanto acumulativo: '))
                k33 = 1 + k3_
                k1 = k3 * k33 ** np.floor((t - m * frac_freq) / a3)
            else:
                print('Error')
            if a1 in ('continuo', 'no discreto'):
                valor = sum(k1 * q * v) * v1
            elif a1 in ('no continuo', 'discreto'):
                valor = sum(k1 * q * v)
            else:
                print('ERROR! Operaciòn no permitida.')
        else:
            print('ERROR! Operaciòn no permitida.')

        if capital == 'constante':

            print('=' * 55)
            print('{0:5} {1:10} {2:10} {3:10}'.format('t', 'factor v', 'prob. (q)', 'pagamentos actualizados'))
            for bonita in np.arange(0, len(t)):
                print('{0:2} {1:10} {2:10} {3:10}'.format(bonita, (np.around(v[bonita], 5)),
                                                          np.around(q[bonita], 5),
                                                          np.around(k1 * q[bonita] * v[bonita], 2)))
            print('=' * 55)
            print('El Valor del seguro de fallecimento es: ', round(valor, 2))
            print('=' * 55)
        elif capital != 'constante':

            print('=' * 55)
            print('{0:5} {1:10} {2:10} {3:10}'.format('t', 'factor v', 'prob. (q)', 'pagamentos actualizados'))
            for bonita in np.arange(0, len(t)):
                print('{0:2} {1:10} {2:10} {3:10}'.format(bonita, (np.around(v[bonita], 5)),
                                                          np.around(q[bonita], 5),
                                                          np.around(k1[bonita] * q[bonita] * v[bonita], 2)))
            print('=' * 55)
            print('El Valor del seguro de fallecimento es: ', round(valor, 2))
            print('=' * 55)  ### Valor del seguro de fallecimiento!

    def renta_constante(self, tabla_mortalidad, x: int, n: int = 120, m: int = 0,
                        h: int = 1, capital: float = 5000, interest: float = .02,
                        birth_year: int = 1975, pospagable: str = 'no'):
        """

        Esta funciòn càlcula el valor actual actuarial de una renta de supervivencia constante.

        :param tabla_mortalidad:  Tabla de mortalidad generacionales PERM.

        :param x:  Edad del individuo.

        :param n:  Temporalidad de la operaciòn.

        :param m:  Diferimiento de la operaciòn.

        :param h:  Frecuencia de fraccionamiento.

        :param capital: Dinero - Capital empleado.

        :param interest: Base técnicas.

        :param birth_year: Ano de nacimiento del individuo.

        :param pospagable: Renta pospagable o prepagable (default).

        :return: El valor actual actuarial de la renta de supervivencia con capital constante.

        """
        datatable = tabla_mortalidad
        frac_freq = h
        if n == 120:
            n = 120 - (x + m)
        elif n != 120:
            n = n
        else:
            print('Error! Type a new "n" ')
        L = np.repeat(1.0, 121)
        L[0] = 1000000
        fem = datatable.iloc[:, 1] * np.exp(-datatable.iloc[:, 2] * (birth_year + np.arange(0, 121) - 2012))
        macho = datatable.iloc[:, 3] * np.exp(-datatable.iloc[:, 4] * (birth_year + np.arange(0, 121) - 2012))
        tabla = .5 * (fem + macho)
        for i in range(0, 120):
            L[i + 1] = L[i] * (1 - (tabla[i] / 1000))
        L = np.round(L, 4)
        fr = np.arange(frac_freq) / frac_freq
        jon = np.outer(L[1:], fr)
        jon1 = np.outer(L[:-1], (1 - fr))
        jj = (jon + jon1).flatten().round(1)
        if frac_freq != 1:

            if pospagable == 'no':
                t = np.arange((m * h), ((m + n) * h))
                v = (1 + interest) ** -(t / h)
                p = jj[x * h + t] / jj[x * h]
            else:
                t = np.arange((m * h), ((m + n) * h))
                v = (1 + interest) ** -((t + 1) / h)
                p = jj[x * h + t + 1] / jj[x * h]
        else:
            if pospagable == 'no':
                t = np.arange(m, (m + n))
                v = (1 + interest) ** - t
                p = L[x + t] / L[x]
            else:
                t = np.arange(m, (m + n))
                v = (1 + interest) ** - (t + 1)
                p = L[x + t + 1] / L[x]

        renta = round(sum(capital * v * p), 2)

        print('=' * 55)
        print('{0:5} {1:10} {2:10} {3:10} {4:10}'.format('t', 'Factor v', 'prob. (q)', 'Pagamentos', 'Cuantias'))
        for bonita in np.arange(0, len(t)):
            print('{0:2} {1:10} {2:10} {3:10} {4:10}'.format(bonita, (np.around(v[bonita], 5)),
                                                             np.around(p[bonita], 5),
                                                             capital,
                                                             np.around(capital * p[bonita] * v[bonita], 2)))
        print('=' * 55)
        print('El valor de la renta de supervivencia es: ', round(renta, 2))
        print('=' * 55)

        return renta  # Valor actual actuarial de la renta constante

    def renta_aritmetica(self, tabla_mortalidad, x: int, n: int = 120, m: int = 0,
                         h: int = 1, capital: float = 500, u1: float = 50, interest: float = .02,
                         birth_year: int = 1964, pospagable: str = 'no'):
        """

        Esta funciòn permite calcular una renta de supervivencia variable linealmente o aritmeticamente
        con frecuencia de variaciòn de pago y cuantìa igual.

        :param tabla_mortalidad:  Tabla de mortalidad generacionales PERM.

        :param x:  Edad del individuo.

        :param n:  Temporalidad de la operaciòn.

        :param m:  Diferimiento de la operaciòn.

        :param h:  Frecuencia de variación de los términos dentro del año. Proporciona el número de
                    veces que varían los términos dentro del año.

        :param capital: Primer término de la operaciòn.

        :param u1:  Segundo termino de la operaciòn.

        :param interest:  Base Técnica.

        :param birth_year: Ano de nacimiento del individuo.

        :param pospagable: Renta pospagable o prepagable (default).

        :return: El valor actual actuarial de la renta de supervivencia variable linealmente.

        """

        datatable = tabla_mortalidad
        frac_freq = h
        if n != 120:
            n = n
        elif n == 120:
            n = 120 - (x + m)
        else:
            print('Error! Type a new "n" ')
        L = np.repeat(1.0, 121)
        L[0] = 1000000
        fem = datatable.iloc[:, 1] * np.exp(-datatable.iloc[:, 2] * (birth_year + np.arange(0, 121) - 2012))
        macho = datatable.iloc[:, 3] * np.exp(-datatable.iloc[:, 4] * (birth_year + np.arange(0, 121) - 2012))
        tabla = .5 * (fem + macho)
        for i in range(0, 120):
            L[i + 1] = L[i] * (1 - (tabla[i] / 1000))
        L = np.round(L, 4)

        if frac_freq != 1:

            fr = np.arange(frac_freq) / frac_freq
            jon = np.outer(L[1:], fr)
            jon1 = np.outer(L[:-1], (1 - fr))
            jj = (jon + jon1).flatten().round(1)
            t = np.arange((m * h), ((m + n) * h))
            if pospagable == 'no':
                v = (1 + interest) ** -(t / h)
                p = jj[x * h + t] / jj[x * h]
            elif pospagable == 'si':
                v = (1 + interest) ** -((t + 1) / h)
                p = jj[x * h + t + 1] / jj[x * h]
            else:
                print('Pospagable acepta solamente "no" y "si"')

        elif frac_freq == 1:
            t = np.arange(m, ((m + n)))
            if pospagable == 'no':
                v = (1 + interest) ** -t
                p = L[x + t] / L[x]
            elif pospagable == 'si':
                v = (1 + interest) ** -(t + 1)
                p = L[x + t + 1] / L[x]
            else:
                print('Pospagable acepta solamente "no" y "si"')

        cap = capital + u1 * (t - m * h)
        renta = round(sum(cap * v * p), 2)

        print('=' * 55)
        print('{0:5} {1:10} {2:10} {3:10} {4:10}'.format('t', 'Factor v', 'prob. (q)', 'Pagamentos', 'Cuantias'))
        for bonita in np.arange(0, len(t)):
            print('{0:2} {1:10} {2:10} {3:10} {4:10}'.format(bonita, (np.around(v[bonita], 5)),
                                                             np.around(p[bonita], 5),
                                                             np.around(cap[bonita], 2),
                                                             np.around(cap[bonita] * p[bonita] * v[bonita], 2)))
        print('=' * 55)
        print('El valor de la renta de supervivencia es: ', round(renta, 2))
        print('=' * 55)

        return renta

    def renta_aritmetica2(self, tabla_mortalidad, x: int, n: int = 120, m: int = 0,
                          h: int = 1, h1: int = 1, capital: float = 500, u1: float = 20, interest: float = .02,
                          birth_year: int = 1964, pospagable: str = 'no'):
        """
        Esta funciòn permite calcular una renta de supervivencia variable linealmente con distinta frecuencia de
        variaciòn de pago y cuantìa.

        :param tabla_mortalidad:  Tabla de mortalidad generacionales PERM.

        :param x:  Edad del individuo.

        :param n:  Temporalidad de la operaciòn.

        :param m:  Diferimiento de la operaciòn.

        :param h:  Frecuencia de variación de los términos dentro del año. Proporciona el número de
                    veces que varían los términos dentro del año.

        :param h1: Frecuencia de pago de los términos de la renta dentro del año. Proporciona el
                    número de términos de la renta que hay en un año.
        :param capital: Primer término de la operaciòn.

        :param u1:  Segundo termino de la operaciòn.

        :param interest:  Base Técnica

        :param birth_year: Año de nacimiento del individuo

        :param pospagable: Renta pospagable o prepagable (default).

        :return: El valor actual actuarial de la renta de supervivencia variable linealmente.

        """
        datatable = tabla_mortalidad
        k = h1 / h
        frac_freq = h * k
        if n != 120:
            n = n
        elif n == 120:
            n = 120 - (x + m)
        else:
            print('Error! Type a new "n" ')
        L = np.repeat(1.0, 121)
        L[0] = 1000000
        fem = datatable.iloc[:, 1] * np.exp(-datatable.iloc[:, 2] * (birth_year + np.arange(0, 121) - 2012))
        macho = datatable.iloc[:, 3] * np.exp(-datatable.iloc[:, 4] * (birth_year + np.arange(0, 121) - 2012))
        tabla = .5 * (fem + macho)
        for i in range(0, 120):
            L[i + 1] = L[i] * (1 - (tabla[i] / 1000))
        L = np.round(L, 4)
        if frac_freq != 1:
            fr = np.arange(frac_freq) / frac_freq
            jon = np.outer(L[1:], fr)
            jon1 = np.outer(L[:-1], (1 - fr))
            jj = (jon + jon1).flatten().round(1)
            if pospagable == 'no':
                t = np.arange((m * h * k), ((m + n) * h * k), dtype='int')
                v = (1 + interest) ** -(t / h1)
                p = jj[x * h1 + t] / jj[x * h1]
            else:
                t = np.arange((m * h * k), ((m + n) * h * k))
                v = (1 + interest) ** -((t + 1) / h * k)
                p = jj[x * h1 + t + 1] / jj[x * h1 * k]

        cap = capital + u1 * np.floor(t / k - m * h)

        renta = round(sum(cap * v * p), 2)
        print('=' * 55)
        print('{0:5} {1:10} {2:10} {3:10} {4:10}'.format('t', 'Factor v', 'prob. (q)', 'Pagamentos', 'Cuantias'))
        for bonita in np.arange(0, len(t)):
            print('{0:2} {1:10} {2:10} {3:10} {4:10}'.format(bonita, (np.around(v[bonita], 5)),
                                                             np.around(p[bonita], 5),
                                                             np.around(cap[bonita], 2),
                                                             np.around(cap[bonita] * p[bonita] * v[bonita], 2)))
        print('=' * 55)
        print('El valor de la renta de supervivencia es: ', round(renta, 2))
        print('=' * 55)

        return renta

    def renta_geometrica(self, tabla_mortalidad, x: int, n: int = 120, m: int = 0,
                         h: int = 1, capital: float = 500, q0: float = .015, interest: float = .02,
                         birth_year: int = 1964, pospagable: str = 'no'):
        """
        Esta funciòn permite calcular una renta de supervivencia variable geometricamente con
        misma frecuencia de variaciò de cuantìa y pago.

        :param tabla_mortalidad:  Tabla de mortalidad generacionales PERM.

        :param x:  Edad del individuo.

        :param n:  Temporalidad de la operaciòn.

        :param m:  Diferimiento de la operaciòn.

        :param h:  Frecuencia de variación de los términos dentro del año. Proporciona el número de
                    veces que varían los términos dentro del año.

        :param capital:  Primer término de la renta de supervivencia.

        :param q0:  Tanto acumulativo.

        :param interest:  Base técnica.

        :param birth_year: Año de nacimiento del individuo.

        :param pospagable: Renta pospagable o prepagable (default).

        :return: El valor actual actuarial de la renta de supervivencia variable geometricamente.

        """

        datatable = tabla_mortalidad
        frac_freq = h
        if n == 120:
            n = 120 - (x + m)
        elif n != 120:
            n = n
        else:
            print('Error! Type a new "n" ')
        L = np.repeat(1.0, 121)
        L[0] = 1000000
        # fr = np.arange(frac_freq) / frac_freq
        fem = datatable.iloc[:, 1] * np.exp(-datatable.iloc[:, 2] * (birth_year + np.arange(0, 121) - 2012))
        macho = datatable.iloc[:, 3] * np.exp(-datatable.iloc[:, 4] * (birth_year + np.arange(0, 121) - 2012))
        tabla = .5 * (fem + macho)
        for i in range(0, 120):
            L[i + 1] = L[i] * (1 - (tabla[i] / 1000))
        L = np.round(L, 4)
        if frac_freq != 1:

            fr = np.arange(frac_freq) / frac_freq
            jon = np.outer(L[1:], fr)
            jon1 = np.outer(L[:-1], (1 - fr))
            jj = (jon + jon1).flatten().round(1)
            t = np.arange((m * h), ((m + n) * h))
            if pospagable == 'no':
                v = (1 + interest) ** -(t / h)
                p = jj[x * h + t] / jj[x * h]
            elif pospagable == 'si':
                v = (1 + interest) ** -((t + 1) / h)
                p = jj[x * h + t + 1] / jj[x * h]
            else:
                print('Pospagable acepta solamente "no" y "si"')

        elif frac_freq == 1:
            t = np.arange(m, (m + n))
            if pospagable == 'no':
                v = (1 + interest) ** -t
                p = L[x + t] / L[x]
            elif pospagable == 'si':
                v = (1 + interest) ** -(t + 1)
                p = L[x + t + 1] / L[x]
            else:
                print('Pospagable acepta solamente "no" y "si"')

        qux = (1 + q0)
        cap = capital * qux ** (t - m * h)

        renta = round(sum(cap * v * p), 2)
        print('=' * 55)
        print('{0:5} {1:10} {2:10} {3:10} {4:10}'.format('t', 'Factor v', 'prob. (q)', 'Pagamentos', 'Cuantias'))
        for bonita in np.arange(0, len(t)):
            print('{0:2} {1:10} {2:10} {3:10} {4:10}'.format(bonita, (np.around(v[bonita], 5)),
                                                             np.around(p[bonita], 5),
                                                             np.around(cap[bonita], 2),
                                                             np.around(cap[bonita] * p[bonita] * v[bonita], 2)))
        print('=' * 55)
        print('El valor de la renta de supervivencia es: ', round(renta, 2))
        print('=' * 55)

        return renta

    def renta_geometrica2(self, tabla_mortalidad, x: int, n: int = 120, m: int = 0,
                          h: int = 1, h1: int = 1, capital: float = 500, q0: float = .015, interest: float = .02,
                          birth_year: int = 1964, pospagable: str = 'no'):
        """

        Esta funciòn permite calcular una renta de supervivencia variable geometricamente con distinta frecuencia
        de variaciòn de cuantìa y pago.

        :param tabla_mortalidad:  Tabla de mortalidad generacionales PERM.

        :param x:  Edad del individuo.

        :param n:  Temporalidad de la operaciòn.

        :param m:  Diferimiento de la operaciòn.

        :param h:  Frecuencia de variación de los términos dentro del año. Proporciona el número de
                    veces que varían los términos dentro del año.

        :param h1: Frecuencia de pago de los términos de la renta dentro del año. Proporciona el
                    número de términos de la renta que hay en un año.

        :param capital:  Primer término de la renta de supervivencia.

        :param q0:  Tanto acumulativo.

        :param interest:  Base técnica.

        :param birth_year: Año de nacimiento del individuo.

        :param pospagable: Renta pospagable o prepagable (default).

        :return: El valor actual actuarial de la renta de supervivencia variable geometricamente.

        """
        datatable = tabla_mortalidad
        k = h1 / h
        frac_freq = h * k
        if n == 120:
            n = n - x
        elif n != 120:
            n = 120 - (x + m)
        else:
            print('Error! Type a new "n" ')
        L = np.repeat(1.0, 121)
        L[0] = 1000000
        fem = datatable.iloc[:, 1] * np.exp(-datatable.iloc[:, 2] * (birth_year + np.arange(0, 121) - 2012))
        macho = datatable.iloc[:, 3] * np.exp(-datatable.iloc[:, 4] * (birth_year + np.arange(0, 121) - 2012))
        tabla = .5 * (fem + macho)
        for i in range(0, 120):
            L[i + 1] = L[i] * (1 - (tabla[i] / 1000))
        L = np.round(L, 4)
        if frac_freq != 1:
            fr = np.arange(frac_freq) / frac_freq
            jon = np.outer(L[1:], fr)
            jon1 = np.outer(L[:-1], (1 - fr))
            jj = (jon + jon1).flatten().round(1)
            if pospagable == 'no':
                t = np.arange((m * h * k), ((m + n) * h * k), dtype='int')
                v = (1 + interest) ** -(t / h1)
                p = jj[x * h1 + t] / jj[x * h1]
            else:
                t = np.arange((m * h * k), (n * h * k))
                v = (1 + interest) ** -((t + 1) / h * k)
                p = jj[x * h1 + t + 1] / jj[x * h1 * k]

        qux = (1 + q0)
        cap = capital * qux ** np.floor(t / k - m * h)

        renta = round(sum(cap * v * p), 2)
        print('=' * 55)
        print('{0:5} {1:10} {2:10} {3:10} {4:10}'.format('t', 'Factor v', 'prob. (q)', 'Pagamentos', 'Cuantias'))
        for bonita in np.arange(0, len(t)):
            print('{0:2} {1:10} {2:10} {3:10} {4:10}'.format(bonita, (np.around(v[bonita], 5)),
                                                             np.around(p[bonita], 5),
                                                             np.around(cap[bonita], 2),
                                                             np.around(cap[bonita] * p[bonita] * v[bonita], 2)))
        print('=' * 55)
        print('El valor de la renta de supervivencia es: ', round(renta, 2))
        print('=' * 55)

        return renta

    def vida_media_diferida(self, cohorte, x=65, m=10, kind='completa'):  ## Vida media temporal |abreviada - complete

        """
        Es el nùmero medio de años que por término medio vivirà un persona de edad x a partir de la edad x+t.
        Dentro de la pràctica de los seguros la vida media o vida media diferida aparece con frecuencia.
        Por ejemplo, supòngase que una persona contrata a los 30 años una plan de pensiones, a cobrar a partir
        de la jubilaciòn (65). Se desearìa conocer cùal es el nùmero de años que dicha persona vivirà tras la jubilaciòn.

        :param cohorte: La funciòn cohorte (lx). The cohort function (lx)

        :param x: La edad del individuo. The age of the individual x. By Default 65.

        :param m: The deferred period. El periodo de diferimiento. By Default 10.

        :param kind: Kind of mean life expectancy, "complete" or "curtate". "Completa" o "Abreviada"

        :return: The deferred mean life expectancy.

        """
        t = pd.Series(np.arange(m + 1, (120 - x)))
        c1 = (cohorte[x + t].sum()) / cohorte[x]
        if kind == 'complete':
            return c1.round(4) + (.5 * cohorte[x + m] / cohorte[x]).round(4)
        elif kind == 'curtate':
            return c1.round(4)
        else:
            print('Error! Kind parameter only accepts "complete" or "curtate"')

    def vida_media_temporal(self, cohorte, x=25, n=5, kind='complete'):  ## pagina 50

        """
        Se trata ahora del nùmero de años que port término medio vivirà una persona de edad x en un intervalo de edades
        (x, x+t).

        :param cohorte: Funciòn cohorte (lx).

        :param x: La edad del individuo.

        :param n: La temporalidad a evaluar.

        :param kind: El tipo "completo" o "abreviado"

        :return: El valor de la vida media temporal

        """
        if kind == 'complete':
            t = pd.Series(np.arange(1, n))
            c1 = (cohorte[x + t].sum()) / cohorte[x]
            c2 = c1 + .5 + .5 * (cohorte[x + n] / cohorte[x])
            return c2.round(7)
        elif kind == 'curtate':
            t = pd.Series(np.arange(1, (n + 1)))
            c1 = (cohorte[x + t].sum()) / cohorte[x]
            return c1.round(7)
        else:
            print('Error! Kind parameter only accepts "complete" or "curtate"')

    def vida_media_mixta(self, cohorte, x=25, m=10, n=5, kind='complete'):  ## Pagina 51 Estadistica actuarial vida

        """
        Se trata ahora del nùmero de años que vivirà una persona de edad x en un intervalo de edades (x+m, x+m+n).

        :param cohorte: La funcin cohorte (lx). The cohort function (lx)

        :param x: La edad del individuo. The age of the individual x

        :param m: The deferred period. El periodo de diferimiento.

        :param n: El periodo hasta la evaluaciòn. The period until which the age should be evaluated

        :param kind: El tipo

        :return: La vida media mixta.

        """
        if kind == 'complete':
            t = pd.Series(np.arange((m + 1), (m + n)))
            c1 = (cohorte[x + t].sum()) / cohorte[x]
            c2 = .5 * (cohorte[x + m] / cohorte[x]) + .5 * (cohorte[x + m + n] / cohorte[x])
            return (c2 + c1).round(7)
        elif kind == 'curtate':
            t = pd.Series(np.arange((m + 1), (m + n + 1)))
            c1 = (cohorte[x + t].sum()) / cohorte[x]
            return c1.round(7)
        else:
            print('Error! Kind parameter only accepts "complete" or "curtate"')


class InsuranceBenefits:

    """

    This class computes basic actuarial operation such as annuity and life insurance.

    It can also computes commutations.

    """

    def pure_endowment(self, cohort, age: int, n: int = 1,
                       i: float = .02, capital: float = 1):  # Exn
        """
        Function to evaluate the pure endowment.

        Funciòn que evalua el Dotal Puro o Capital diferifo.

        :param capital: Int or Float. The capital.

        :param cohort: Array-like. The cohort function (lx).

        :param age: Int. It is the age of the insured.

        :param n: Int. Length of the contract.

        :param i: Interest Rate.

        :return: The Actuarial Present Value of the contract and the probability Exn.

        """

        time = n
        factor = 1 / (1 + i) ** time
        s = age + time
        probability = np.roll(cohort[s], 1) / cohort[age]
        n_ex = round(factor * probability, 7)
        endow = n_ex * capital
        print(f'The Pure Endowment and value for an individual aged {age} \n'
              f'with a length contract of {time} given {capital} bucks is:\n')
        return round(endow, 2), n_ex  # Value of Pure Endowment without calculation

    def increasing_annuity(self, cohort, x, m=0, i=.02,
                           payments: str = 'advance'):

        """

        This function evaluates increasing annuities.

        :param cohort: The cohort function (lx).

        :param x: The age of insured

        :param m: The deferred period.

        :param i: Interest Rate.

        :param payments: The kind of increasing annuity. "advance" or "arrears" are accepted.

        :return:  The increasing annuity (advance or arrears).

        """
        dx = (cohort - cohort.shift(-1)).fillna(0)
        indice = pd.Series(range(1, len(cohort))).fillna(0)
        # Cx = ((1 + i) ** (-indice) * dx).fillna(0)
        Dx = (1 + i) ** (-cohort.index) * cohort

        Nx = []
        for valor in range(0, len(Dx)):
            Nx.append(sum(Dx[valor:]))

        Sx = []
        for s in range(0, len(Nx)):
            Sx.append(sum(Nx[s:]))
        if payments == 'advance':
            iaxn = (Sx[x + m]) / Dx[x]
        elif payments == 'arrears':
            iaxn = (Sx[x + m + 1]) / Dx[x]
        return iaxn

    def increasing_lifeinsurance(self, cohort, age, n=0, m=0, i=.02, kind='whole'):

        """

        :param cohort: The cohort function (lx).

        :param age: The age of insured

        :param n: The time of evaluation.

        :param m: The deferred period.

        :param i: Interest Rate.

        :param kind: The kind of increasing life insurance. "Whole" or "Temporary" are accepted.

        :return: The increasing life insurance.

        """
        dx = (cohort - cohort.shift(-1)).fillna(0)
        indice = pd.Series(range(1, len(cohort))).fillna(0)
        Cx = ((1 + i) ** (-indice) * dx).fillna(0)
        Dx = (1 + i) ** (-cohort.index) * cohort

        Nx = []
        for valor in range(0, len(Dx)):
            Nx.append(sum(Dx[valor:]))
        Mx = []
        for x in range(0, len(Cx)):
            Mx.append(sum(Cx[x:-1]))
        Sx = []
        for s in range(0, len(Nx)):
            Sx.append(sum(Nx[s:]))
        Rx = []
        for r in range(0, len(Mx)):
            Rx.append(sum(Mx[r:]))
        if kind == 'whole':
            ias = Rx[age + m] / Dx[age]
            return round(ias, 6)
        elif kind == 'temporary':
            ias = (Rx[age + m] - Rx[age + n + m] - n * Mx[age + n + m]) / Dx[age]
            return round(ias, 6)
        else:
            print('Error! "Kind" can be "whole" or "temporary" either')

    def decreasing_annuity(self, cohort, age, m=0, n=1, i=.02, payments='advance'):

        """

        :param cohort: The cohort function (lx).

        :param age: The age of insured

        :param n: The time of evaluation.

        :param m: The deferred period.

        :param i: Interest Rate.

        :param payments: The kind of payments. It can be "advance" or "arrears".

        :return: The decreasing annuity.

        """

        x = age
        dx = (cohort - cohort.shift(-1)).fillna(0)
        indice = pd.Series(range(1, len(cohort))).fillna(0)
        Cx = ((1 + i) ** (-indice) * dx).fillna(0)
        Dx = (1 + i) ** (-cohort.index) * cohort

        Nx = []
        for valor in range(0, len(Dx)):
            Nx.append(sum(Dx[valor:]))

        Sx = []
        for s in range(0, len(Nx)):
            Sx.append(sum(Nx[s:]))

        if payments == 'advance':
            daxn = ((n * Nx[x]) - (Sx[x + m + 1] - Sx[x + m + n + 1])) / Dx[x]
        elif payments == 'arrears':
            daxn = ((n * Nx[x + 1]) - (Sx[x + m + 2] - Sx[x + m + n + 2])) / Dx[x]
        else:
            print('Error! Insert right "advance" or "arrears" ')
        return daxn

    def temporary_annuity(self, cohort, age: int, n: int = 'whole', m=1,
                          i: float = .02, capital: float = 1, payments: str = 'advance'):  # axn

        """

        Temporary annuity function.
        Annuity advance and arrears can be evaluated.
        This function calculates actuarial value of annuities, given a cohort.
        Por defecto càlcula la annuity-advance, puede pasarsele la arrears.

        :param capital: Int or Float. The capital.

        :param payments: The kind of annuity "arrears" or "advance".

        :param cohort: Array-like. The cohort function (lx).

        :param age: Int. It is the age of the insured.

        :param n: Int. Length of the contract. If missing is assumed until omega.

        :param m: Number of fractional payments per period. By default 1.

        :param i: Interest Rate.

        :return: Temporary annuity.

        """

        def omegas():
            omega1 = 0

            if int(cohort[-1:]) != 0:
                omega1 = cohort.index[-1] + 1
            else:
                omega1 = cohort.index[-1]
            return omega1

        # omegas()
        if n != 'whole':
            n = n
        elif n == 'whole':
            n = omegas() - (age + m)
        else:
            print('Error! Type a new "n" ')

        ## Imprentando tomar la temporalidad
        time = n
        Dx = (1 + i) ** (-cohort.index) * cohort
        w = len(Dx)
        nex = Dx[age + n] / Dx[age]  ## Dotal Puro
        konstante = (m - 1) / (2 * m)
        Nx = []
        for valor in range(0, w):
            Nx.append(sum(Dx[valor:]))

        if payments == 'arrears':
            print('The actuarial value of this annuity-arrears is:')
            axn = (Nx[age + 1] - Nx[age + time + 1]) / Dx[age]
            axn1 = axn + konstante * (1 - nex)  ## Using Approximation
            return round(axn1 * capital, 5)
        elif payments == 'advance':
            print('The actuarial value of this annuity-advance is:')
            axn2 = (Nx[age] - Nx[age + time]) / Dx[age]
            axn3 = axn2 - konstante * (1 - nex)  ## Using Approximation
            return round(axn3 * capital, 5)
        else:
            print('Payments parameter should be advance (default) or arrears either')

    def deferred_annuity(self, cohort, age: int, n: int = 10,
                         m: int = 5, i: float = .02, capital: float = 1,
                         payments='advance'):
        """

        :param capital: Float. The capital.

        :param cohort: Array-like. The cohort function (lx).

        :param age: Int. It is the age of the insured.

        :param n: Int. Length of the contract.

        :param m: Int. The deferred period.

        :param i: Interest Rate.

        :param payments:  The kind

        :return:

        """

        time = n
        Dx = (1 + i) ** (-cohort.index) * cohort
        n = len(Dx)
        Nx = []
        for valor in range(0, n):
            Nx.append(sum(Dx[valor:]))
        if payments == 'arrears':
            axn = (Nx[age + m + 1] - Nx[age + m + time + 1]) / Dx[age]
            return round(axn * capital, 5)
        elif payments == 'advance':
            axn2 = (Nx[age + m] - Nx[age + m + time]) / Dx[age]
            return round(axn2 * capital, 5)
        elif payments == 'whole arrears':
            axn3 = Nx[age + m + 1] / Dx[age]
            return round(axn3 * capital, 5)
        elif payments == 'whole advance':
            axn3 = Nx[age + m] / Dx[age]
            return round(axn3 * capital, 5)
        else:
            print('Please the payments should be specified as "advance", "arrears", "whole advance" or '
                  '"whole arrears" either')

    def commutations(self, cohort, i: float = .02):
        """

        Tabulates the actuarial commutation functions.

        Calcula las communtaciones dada una coorte y tasa i.

        :param cohort: The cohort function (lx).

        :param i: Float. Interest Rate.

        :return: The table of commutations given i (rate).

        """

        dx = (cohort - cohort.shift(-1)).fillna(0)
        indice = pd.Series(range(1, len(cohort))).fillna(0)
        Cx = ((1 + i) ** (-indice) * dx).fillna(0)
        Dx = (1 + i) ** (-cohort.index) * cohort

        Nx = []
        for valor in range(0, len(Dx)):
            Nx.append(sum(Dx[valor:]))
        Mx = []
        for x in range(0, len(Cx)):
            Mx.append(sum(Cx[x:-1]))
        Sx = []
        for s in range(0, len(Nx)):
            Sx.append(sum(Nx[s:]))
        Rx = []
        for r in range(0, len(Mx)):
            Rx.append(sum(Mx[r:]))

        df = pd.DataFrame({'lx': cohort, 'Dx': Dx, 'Nx': Nx,
                           'Cx': Cx, 'Mx': Mx, 'Rx': Rx, 'Sx': Sx})
        print('--' * 25)
        print(f'Commutations results of {cohort.name}:')
        print('--' * 25)
        print('Date and Time: ', strftime("%a, %d %b %Y %H:%M:%S"))
        print('Region and Country: ', geo_json['region'], ',', geo_json['country'])
        return df  ## Commutations

    def endowment(self, cohort, age: int, t: int = 1, i: float = .02,
                  capital: float = 1):  # AExn
        """

        Function to evaluate the n-year endowment insurance.

        :param cohort: The cohort function (lx).

        :param age: Int. Age of the insured.

        :param t: The length of the contract.

        :param i: Interest Rate.

        :param capital: Float. The capital of the operation.

        :return:  The endowment.

        """
        time = t
        fee = capital
        dx = (cohort - cohort.shift(-1)).fillna(0)
        indice = pd.Series(range(1, len(cohort))).fillna(0)
        Cx = ((1 + i) ** (-indice) * dx).fillna(0)
        Dx = (1 + i) ** (-cohort.index) * cohort
        Mx = []
        for x in range(0, len(Cx)):
            Mx.append(sum(Cx[x:-1]))
        pagamento = (Mx[age] - Mx[age + time] + Dx[age + time]) / Dx[age]
        tariffa = round(pagamento * fee, 2)
        print(f'The endowment of age {age}: is {tariffa} and his probability is {pagamento}')
        return tariffa

    def tincreasing_annuity(self, cohort, x, m=0, n=1, i=.02,
                            payments: str = 'advance'):  ## m deferred period.

        dx = (cohort - cohort.shift(-1)).fillna(0)
        indice = pd.Series(range(1, len(cohort))).fillna(0)
        Cx = ((1 + i) ** (-indice) * dx).fillna(0)
        Dx = (1 + i) ** (-cohort.index) * cohort

        Nx = []
        for valor in range(0, len(Dx)):
            Nx.append(sum(Dx[valor:]))

        Sx = []
        for s in range(0, len(Nx)):
            Sx.append(sum(Nx[s:]))

        if payments == 'advance':
            iaxn = (Sx[x + m] - Sx[x + n + m] - n * Nx[x + n + m]) / Dx[x]
        elif payments == 'arrears':
            iaxn = (Sx[x + m] - Sx[x + m + n + 1] - n * Nx[x + n + m + 1]) / Dx[x]
        return iaxn

    def whole_life_insurance(self, cohort, age, i: float = .02,
                             capital: float = 1, kind: str = 'whole'):
        """

         A payment of 1 is made at the end of the year of death of a person
            aged x.

        :param cohort: The cohort function (lx).

        :param age: The Age of the individual.

        :param i: Interest Rate.

        :param capital: The capital of the operation.

        :param kind: The kind of life insurance contract. "Whole" or "Immediate".

        :return:  The present value of the payment of the whole life insurance.

        """

        dx = (cohort - cohort.shift(-1)).fillna(0)
        indice = pd.Series(range(1, len(cohort))).fillna(0)
        Cx = ((1 + i) ** (-indice) * dx).fillna(0)
        Dx = (1 + i) ** (-cohort.index) * cohort

        Nx = []
        for valor in range(0, len(Dx)):
            Nx.append(sum(Dx[valor:]))
        Mx = []
        for x in range(0, len(Cx)):
            Mx.append(sum(Cx[x:-1]))
        Sx = []
        for s in range(0, len(Nx)):
            Sx.append(sum(Nx[s:]))
        Rx = []
        for r in range(0, len(Mx)):
            Rx.append(sum(Mx[r:]))

        if kind == 'immediate':
            v = (1 + i) ** .5
            insurance = v * Mx[age] / Dx[age]
        elif kind == 'whole':
            insurance = Mx[age] / Dx[age]
        else:
            print('Only "whole" and "immediate" are accepted!')

        return round(insurance * capital, 7)

    def temporary_insurance(self, cohort, age, m: int = 0, n: int = 1, i: float = .02,
                            capital: float = 1):
        """

        A payment of 1 is made at the end of the year of death of a
        person aged x provided the person dies within n years.

        :param cohort: The cohort function (lx).

        :param age: The age of the individual.

        :param m: The deferred period.

        :param n: Period until which the age should be evaluated.

        :param i: Interest Rate.

        :param capital: The capital.

        :return: The present value of the payments.

        """

        dx = (cohort - cohort.shift(-1)).fillna(0)
        indice = pd.Series(range(1, len(cohort))).fillna(0)
        Cx = ((1 + i) ** (-indice) * dx).fillna(0)
        Dx = (1 + i) ** (-cohort.index) * cohort

        Nx = []
        for valor in range(0, len(Dx)):
            Nx.append(sum(Dx[valor:]))
        Mx = []
        for x in range(0, len(Cx)):
            Mx.append(sum(Cx[x:-1]))
        Sx = []
        for s in range(0, len(Nx)):
            Sx.append(sum(Nx[s:]))
        Rx = []
        for r in range(0, len(Mx)):
            Rx.append(sum(Mx[r:]))

        insurance = (Mx[age + m] - Mx[age + m + n]) / Dx[age]

        return round(insurance * capital, 5)



