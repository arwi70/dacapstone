import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from io import BytesIO
import base64

def load_telco():
    # Read data
    telco = pd.read_csv('data/telcochurn.csv')
    
    # Adjust dtypes
    catcol = telco.select_dtypes('object').columns
    telco[catcol] = telco[catcol].apply(lambda x: x.astype('category'))
    
    # Tenure Months to grouping categories
    def grouping_tenure(telco) :
        if telco["tenure_months"] <= 12 :
            return "< 1 Year"
        elif (telco["tenure_months"] > 12) & (telco["tenure_months"] <= 24 ):
            return "1-2 Year"
        elif (telco["tenure_months"] > 24) & (telco["tenure_months"] <= 48) :
            return "2-4 Year"
        elif (telco["tenure_months"] > 48) & (telco["tenure_months"] <= 60) :
            return "4-5 Year"
        else:
            return "> 5 Year"
        
    telco["tenure_group"] = telco.apply(lambda telco: grouping_tenure(telco), axis = 1) 
    
    # Adjust category order
    tenure_group = ["< 1 Year", "1-2 Year", "2-4 Year", "4-5 Year", "> 5 Year"]
    telco["tenure_group"] = pd.Categorical(telco["tenure_group"], categories = tenure_group, ordered=True)
    
    # Monthly charges to grouping categories
    def grouping_monthly_charges(telco) :
        if telco["monthly_charges"] <= 35.5 :
            return "< 35.5"
        elif (telco["monthly_charges"] > 35.5) & (telco["monthly_charges"] <= 70.35 ):
            return "35.5 - 70.35"
        elif (telco["monthly_charges"] > 70.35) & (telco["monthly_charges"] <= 89.85) :
            return "70.35 - 89.85"
        elif (telco["monthly_charges"] > 89.85) :
            return "> 89.85"
        else:
            return "unknown"

    telco["monthly_charges_group"] = telco.apply(lambda telco: grouping_monthly_charges(telco), axis = 1) 

    # Adjust category order
    monthly_charges_group = ["< 35.5", "35.5 - 70.35", "70.35 - 89.85", "> 89.85", 'unknown']
    telco["monthly_charges_group"] = pd.Categorical(telco["monthly_charges_group"], categories = monthly_charges_group, ordered=True)
    
    return(telco)
	
def table_churn(data):
	table = pd.crosstab(data['churn_label'], columns = 'percent', normalize = True)*100
	return(table)

def plot_phone(data):
    
    # ---- Phone Service Customer
    phone_srv = pd.crosstab(data['phone_service'], data['churn_label'], normalize=True)*100

    ax = phone_srv.plot(kind = 'barh', color=['#53a4b1','#c34454'], figsize = (8,6))

    # Plot Configuration
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())
    plt.legend(['Retain', 'Churn'],fancybox=True,shadow=True)
    plt.axes().get_yaxis().set_label_text('')
    plt.title('Phone Service Customer')
    
    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png', transparent=True)
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_internet(data):

    # ---- Internet Service Customer
    inet = pd.crosstab(data['internet_service'], data['churn_label'], normalize=True)*100

    ax = inet.plot(kind = 'barh', color=['#53a4b1','#c34454'], figsize = (8,6))

    # Plot Configuration
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())
    plt.legend(['Retain', 'Churn'],fancybox=True,shadow=True)
    plt.axes().get_yaxis().set_label_text('')
    plt.title('Internet Service Customer')

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_tenure_churn(data):
    
    # ---- Churn Rate by Tenure Group
    crbg = (pd.crosstab(data['tenure_group'], data['churn_label'], normalize=True)*100).round(2)

    ax = crbg.plot(kind = 'bar', color=['#53a4b1','#c34454'], figsize=(8, 6))

    # Plot Configuration
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.axes().get_xaxis().set_label_text('')
    plt.xticks(rotation = 360)
    plt.legend(['Retain', 'Churn'],fancybox=True,shadow=True)
    plt.title('Churn Rate by Tenure Group')

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_tenure_cltv(data):

    # ---- Average Lifetime Value by Tenure
    crbltv = pd.crosstab(data['tenure_months'], data['churn_label'], values=data['cltv'], aggfunc='mean', normalize=False)

    ax = crbltv.plot(color=['#333333','#b3b3b3'], figsize=(8, 6),style = '.--')

    # Plot Configuration
    plt.axes().get_xaxis().set_label_text('Tenure (in Months)')
    plt.title('Average Lifetime Value by Tenure')
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))
    plt.xticks(rotation = 360)
    plt.legend(['Retain', 'Churn'],fancybox=True,shadow=True)

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_contract_churn(data):
    
    # ---- Churn Rate by Contract
    contract = (pd.crosstab(data['tenure_group'], data['churn_label'], normalize=True)*100).round(2)

    ax = contract.plot(kind = 'bar', color=['#53a4b1','#c34454'], figsize=(8, 6))

    # Plot Configuration
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.axes().get_xaxis().set_label_text('')
    plt.xticks(rotation = 360)
    plt.legend(['Retain', 'Churn'],fancybox=True,shadow=True)
    plt.title('Churn Rate by Contract')

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_monthly_charges_churn(data):
    
    # ---- Churn Rate by Monthly Charges Group
    month_charge = pd.crosstab(data['monthly_charges_group'], data['churn_label'], normalize=True)*100

    ax = month_charge.plot(kind = 'bar', color=['#53a4b1','#c34454'], figsize=(8, 6))

    # Plot Configuration
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.axes().get_xaxis().set_label_text('')
    plt.xlabel('Monthly Charge')
    plt.xticks(rotation = 360)
    plt.legend(['Retain', 'Churn'],fancybox=True,shadow=True)
    plt.title('Churn Rate by Monthly Charges Group')

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)
