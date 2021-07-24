# Telma

Welcome to Telma's Library.

![image](https://user-images.githubusercontent.com/67124439/126873444-3ee1e47d-f833-42da-bb75-6c4818c94c66.png)

This library is composed by 5 Classes. Namely:

* BiometricModel.
* OneLife
* MultipleLives
* SpainOperation
* InsuranceBenefits

Plotting functions are located in **OneLife** or **MultiplesLives** classes.

Besides the "classic static" manner of plotting in life actuarial science. **<font color='navy'>Telma</font>** permits plotting charts **interactively.**

---
## Plotting using OneLife and MultipleLives (statically).
---

##### OneLife
It will be possible to graph either from a cohort function or several. <br>
* For plotting **one cohort**,  **OneLife** will be used.<br>
* For plotting **more than one cohorts**, **MultipleLives.** will be used. <br>

Example with one cohort: **Usa_Male**.


Invoking OneLife, *lifeplot* method has as parameters:
* **cohort1**. It refers to the cohort to be passed.
* **interactive**. If true an interactive chart will be plotted using *Plotly*.
* **death**. It refers to the numbers of death chart $d(x)$, if True when plotting interactively it will show the number of death chart.
* **qx_log**. It refers to the probability of death in logarithmic scale, that is $log(q(x))$. If True when plotting interactively it will show $log(q(x))$.

Examples
* OneLife
![image](https://user-images.githubusercontent.com/67124439/126873650-ccbee964-f0c1-4ff0-aaef-117e811b8687.png)

##### Mortality Hump

![image](https://user-images.githubusercontent.com/67124439/126873678-74dd3518-78e4-4265-8c1a-fac9d3fdc5da.png)

---

##### MultipleLives

### The question: do I want to plot more cohorts?
##### Follow the same steps as OneLife ().lifeplot but with:

* MultipleLives -> **lifeplot_2** method
* **Two cohorts**. That is, by default at least two parameters will be needed; $ l_x $ and $l_y$ the cohort functions 
* A third cohort can be passed, if perhaps you want to confront a model.

<br> Example: usa_male, usa_female and a "model".


![image](https://user-images.githubusercontent.com/67124439/126873575-399c4389-3696-48fc-9986-c15a3d094b61.png)
---
# For view some examples interactively please, click the following link. In fact, it is not possible visualize plotly charts from github. 
[1 Plotting Telma](https://nbviewer.jupyter.org/github/Joevalencia/telma/blob/main/1%20Plotting-example.ipynb)
---
### For more examples click the following links:

[BiometricModel](https://github.com/Joevalencia/telma/blob/main/2%20Biometric%20Model%20-%20example.ipynb)

[SpainOperation](https://github.com/Joevalencia/telma/blob/main/3%20SpainOperation%20-%20example.ipynb)

[InsuranceBenefits](https://github.com/Joevalencia/telma/blob/main/4%20Insurance%20Benefits%20-%20example.ipynb)

---
Telma - Documentation [docs](https://htmlpreview.github.io/?https://github.com/Joevalencia/telma/blob/main/telma%20docus.html)
---
