import datetime
import numpy as np
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode,GridUpdateMode
now = int(datetime.datetime.now().timestamp())
start_ts = now - 3 * 30 * 24 * 60 * 60
# @st.cache(allow_output_mutation=True)
# def make_data():
#     df = pd.DataFrame(
#         {
#             "timestamp": np.random.randint(start_ts, now, 20),
#             "side": [np.random.choice(["buy", "sell"]) for i in range(20)],
#             "base": [np.random.choice(["JPY", "GBP", "CAD"]) for i in range(20)],
#             "quote": [np.random.choice(["EUR", "USD"]) for i in range(20)],
#             "amount": list(
#                 map(
#                     lambda a: round(a, 2),
#                     np.random.rand(20) * np.random.randint(1, 1000, 20),
#                     )
#             ),
#             "price": list(
#                 map(
#                     lambda p: round(p, 5),
#                     np.random.rand(20) * np.random.randint(1, 10, 20),
#                     )
#             ),
#             "clicked": [""]*20,
#         }
#     )
#     df["cost"] = round(df.amount * df.price, 2)
#     df.insert(
#         0,
#         "datetime",
#         df.timestamp.apply(lambda ts: datetime.datetime.fromtimestamp(ts)),
#     )
#     return df.sort_values("timestamp").drop("timestamp", axis=1)

cla_df = pd.read_csv(
   # "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
   "./csv_data/final.csv"
   #"./dashboard/csv_data/final.csv"
)
cla_df2 = cla_df[['jc_number','Themes', 'Sub_Themes.1', 'cla_title_en', 'royal_decree_date',  'toepassing', 'loon', 'duur', 'Summary']]

# an example based on https://www.ag-grid.com/javascript-data-grid/component-cell-renderer/#simple-cell-renderer-example
BtnCellRenderer = JsCode('''
class BtnCellRenderer {
    init(params) {
        this.params = params;
        this.eGui = document.createElement('div');
        this.eGui.innerHTML = `
         <span>
            <button id='click-button' 
                class='btn-simple' 
                style='color: ${this.params.color}; background-color: ${this.params.background_color}'>Summarize</button>
         </span>
      `;
        this.eButton = this.eGui.querySelector('#click-button');
        this.btnClickedHandler = this.btnClickedHandler.bind(this);
        this.eButton.addEventListener('click', this.btnClickedHandler);
    }
    getGui() {
        return this.eGui;
    }
    refresh() {
        return true;
    }
    destroy() {
        if (this.eButton) {
            this.eGui.removeEventListener('click', this.btnClickedHandler);
        }
    }
    btnClickedHandler(event) {
        if(this.params.getValue() == 'clicked') {
            this.refreshTable('');
        } else {
            this.refreshTable('clicked');
        }
            console.log(this.params);
            console.log(this.params.getValue());
        }
    refreshTable(value) {
        this.params.setValue(value);
    }
};
''')

df = cla_df2
gb = GridOptionsBuilder.from_dataframe(df, enableRowGroup=True)
gb.configure_default_column(editable=True, min_column_width=100)
gb.configure_column(field='jc_number', header_name='JC Number', supressSizeToFit = 'true')
gb.configure_column(field = 'Themes', header_name='Theme', surpressSizeToFit = 'true')
gb.configure_column(field = 'Sub_Themes.1', header_name='Sub Theme', surpressSizeToFit = 'true')
gb.configure_columns(column_names = ['loon', 'duur', 'toepassing', 'Summary'], hide = 'true' )

grid_options = gb.build()

grid_options['columnDefs'].append({
    #field = column header
    "field": "clicked",
    "header": "Summarize",
    "cellRenderer": BtnCellRenderer,
    "cellRendererParams": {
        "color": "black",
        "background_color": "white",
    },
    'width' : 400
})

st.title("Interactive CLA Finder")

response = AgGrid(df,
                  theme="streamlit",
                  key='table1',
                  gridOptions=grid_options,
                  allow_unsafe_jscode=True,
                  fit_columns_on_grid_load=True,
                  reload_data=False,
                  try_to_convert_back_to_original_types=False
                  )
summary_cell = response['data']['Summary']
#st.write(summary_cell)
try:
    st.write(summary_cell[response['data'].clicked == 'clicked'])
except:
    st.write('Nothing was clicked')
#extra code
#if (confirm('Are you sure you want to CLICK?') == true) {
#     }