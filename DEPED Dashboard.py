
from dash import Dash, html, dcc, Input, Output, State, ctx, callback_context
import plotly.express as px
import dash
import pandas as pd
import base64
import io
from dash.exceptions import PreventUpdate

# Initialize the Dash app
app = Dash(__name__, suppress_callback_exceptions=True)

# =========================================================== STYLING =====================================================================================
# Styling
COLORS = {
    'background': '#f5f5f7',
    'white': '#ffffff',
    'primary': '#00529B',  # Apple blue
    'secondary': '#f56300',  # Orange
    'accent': '#6e6e73',  # Dark gray
    'text': '#1d1d1f',
    'border': '#d2d2d7',
    'success': '#34c759',  # Green
    'warning': '#ff9500',  # Orange/amber
    'error': '#ec1c2d',  # Red
    'purple': '#af52de',
    'light_gray': '#f2f2f2',

    # Colors for the metric cards
    'blue': '#0071e3',  # Male card
    'pink': '#ff375f',  # Female card
    'teal': '#64d2ff',  # Total enrollees
    'green': '#3eb049'  # Total schools
}

# Component styles
upper_header_style = {
    'display': 'flex',
    'alignItems': 'center',
    'justifyContent': 'space-between',
    'padding': '16px 24px',
    'backgroundColor': COLORS['primary'],
    'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
    'borderRadius': '0px',
    'marginBottom': '16px',
    'fontFamily': 'Helvetica Neue, Arial, EB Garamond, sans-serif',
}

header_style = {
    'display': 'flex',
    'alignItems': 'center',
    'justifyContent': 'space-between',
    'padding': '16px 24px',
    'backgroundColor': COLORS['white'],
    'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
    'borderRadius': '12px',
    'marginBottom': '16px',
    'fontFamily': 'Helvetica Neue, Arial, EB Garamond, sans-serif',
}

header_text_style = {
    'marginLeft': '14px',
    'fontWeight': 'normal',
    'color': COLORS['white'],
    'fontFamily': 'Helvetica Neue, Arial, EB Garamond, sans-serif'
}

# Base metric card style
metric_card_style = {
    'backgroundColor': COLORS['white'],
    'padding': '14px',
    'borderRadius': '10px',
    'flex': '1',
    'textAlign': 'center',
    'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
    'display': 'flex',
    'flexDirection': 'column',
    'justifyContent': 'center',
    'alignItems': 'center',
    'transition': 'all 0.2s ease',
    'height': '60px',
    'fontFamily': 'Helvetica Neue, Arial, sans-serif',
}

# Different styled metric cards
male_card_style = {
    **metric_card_style,
    'borderColor': '#616867',
}

female_card_style = {
    **metric_card_style,
    'borderColor': '#616867',
}

total_enrollees_card_style = {
    **metric_card_style,
    'borderColor': '#616867',
}

total_schools_card_style = {
    **metric_card_style,
    'borderColor': '#616867',
}

# Styled metric numbers based on card
male_number_style = {
    'fontSize': '32px',
    'fontWeight': '600',
    'color': '#616867',
    'marginBottom': '4px',
    'fontFamily': 'Helvetica Neue, Arial, sans-serif'
}

female_number_style = {
    'fontSize': '32px',
    'fontWeight': '600',
    'color': '#616867',
    'marginBottom': '4px',
    'fontFamily': 'Helvetica Neue, Arial, sans-serif'
}

total_enrollees_number_style = {
    'fontSize': '32px',
    'fontWeight': '600',
    'color': '#616867',
    'marginBottom': '4px',
    'fontFamily': 'Helvetica Neue, Arial, sans-serif'
}

total_schools_number_style = {
    'fontSize': '32px',
    'fontWeight': '600',
    'color': '#616867',
    'marginBottom': '4px',
    'fontFamily': 'Helvetica Neue, Arial, sans-serif'
}

metric_label_style = {
    'fontSize': '14px',
    'color': COLORS['accent'],
    'fontFamily': 'Helvetica Neue, Arial, sans-serif',
    'fontWeight': '500'
}

status_box_style = {
    'padding': '8px 14px',
    'backgroundColor': COLORS['purple'],
    'color': COLORS['white'],
    'borderRadius': '8px',
    'fontSize': '13px',
    'opacity': '0.9',
    'fontFamily': 'Helvetica Neue, Arial, sans-serif',
    'fontWeight': '500'
}

filters_container_style = {
    'width': '16%',
    'padding': '16px 20px',
    'backgroundColor': COLORS['white'],
    'borderRadius': '12px',
    'marginRight': '5px',
    'color': COLORS['text'],
    'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
    'height': 'fit-content',
    'alignSelf': 'flex-start',
    'fontFamily': 'Helvetica Neue, Arial, sans-serif',
    'position': 'sticky',
    'top': '20px',
    'zIndex': 1
}

button_style = {
    'padding': '10px 16px',
    'border': 'none',
    'borderRadius': '8px',
    'cursor': 'pointer',
    'fontSize': '14px',
    'fontWeight': '500',
    'outline': 'none',
    'textTransform': 'none',
    'height': '40px',
    'margin': '0 10px 0 0',
    'fontFamily': 'Helvetica Neue, Arial, sans-serif',
    'transition': 'all 0.2s ease'
}

primary_button_style = {
    **button_style,
    'backgroundColor': COLORS['primary'],
    'color': 'white',
}

danger_button_style = {
    **button_style,
    'backgroundColor': '#ec1c2d',
    'color': 'white',
}

filter_button_style = {
    **button_style,
    'backgroundColor': '#616867',
    'color': 'white',
    'marginBottom': '16px',
    'width': '100%',
}

filter_label_style = {
    'fontWeight': '600',
    'marginBottom': '4px',
    'marginTop': '10px',
    'fontSize': '13px',
    'fontFamily': 'Helvetica Neue, Arial, sans-serif',
    'color': COLORS['primary']
}

dropdown_style = {
    'marginBottom': '10px',
    'fontFamily': 'Helvetica Neue, Arial, sans-serif',
    'borderRadius': '8px'
}

chart_heading_style = {
    'fontSize': '16px',
    'fontWeight': '700',
    'margin': '0 0 10px 0',
    'fontFamily': 'Helvetica Neue, Arial, sans-serif',
    'color': COLORS['primary']
}

chart_style = {
    'backgroundColor': COLORS['white'],
    'borderRadius': '12px',
    'padding': '16px 20px',
    'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
    'marginBottom': '16px',
    'fontFamily': 'Helvetica Neue, Arial, sans-serif',
    'width': '100%'
}

# Enhanced styles for chart sections
enrollment_chart_style = {
    'backgroundColor': COLORS['white'],
    'borderRadius': '12px',
    'padding': '16px 20px',
    'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
    'marginBottom': '16px',
    'fontFamily': 'Helvetica Neue, Arial, sans-serif',
    'height': '275px'
}

# =========================================================== END OF STYLING =============================================================================

# =========================================================== LAYOUTS =====================================================================================
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Main Dashboard Layout
main_dashboard_layout = html.Section([
    dcc.Store(id='stored-data'),

    # Header with Logo
    html.Div([
        # Left side with logo and title
        html.Div([
            html.Img(
                src='https://upload.wikimedia.org/wikipedia/commons/f/fa/Seal_of_the_Department_of_Education_of_the_Philippines.png',
                style={'height': '100px', 'marginRight': '8px'}
            ),
            html.Div([
                html.H1("REPUBLIC OF THE PHILIPPINES",
                        style={'fontFamily': "'EB Garamond', serif", 'fontSize': '22px', 'margin': '0', 'marginBottom': '3px', 'fontWeight': '400'}),
                html.H2("DEPARTMENT OF EDUCATION",
                        style={'fontFamily': "'EB Garamond', serif", 'fontSize': '36px', 'margin': '0', 'fontWeight': '500'})
            ], style=header_text_style)
        ], style={'display': 'flex', 'alignItems': 'center'}),

        # Right side status
        html.Div(id='header-status', style={'color': COLORS['accent'], 'fontSize': '13px'}),

    ], style={
        **upper_header_style,
        'display': 'flex',
        'justifyContent': 'space-between',
        'alignItems': 'center'
    }),

    html.Div([
        html.H3("School Enrollment Dashboard",
                style={'fontFamily': 'Arial, sans-serif',
                       'color': COLORS['primary'],
                       'fontWeight': 'bold',
                       'fontSize': '40px',
                       'margin': '24px 0',
                       'marginLeft' : '20px',
                       'textAlign': 'left'})
    ]),

    # Upload Controls and Compare Button
    html.Div([
        # Left side with upload controls
        html.Div([
            dcc.Upload(
                id='upload-dataset',
                children=html.Button('Upload Data', style=primary_button_style),
                multiple=False
            ),
            html.Button('Clear Data', id='clear-btn', style=danger_button_style),
            html.Div(id='output-upload')
        ], style={'display': 'flex', 'alignItems': 'center', 'gap': '10px', 'flex': '1'}),

        # Right side with compare button
        dcc.Link(
            html.Button('Compare Dashboard', style={
                **button_style,
                'backgroundColor': COLORS['green'],
                'color': 'white',
                'marginRight': 'auto'
            }),
            href='/comparison-dashboard'
        )
    ], style={
        **header_style,
        'display': 'flex',
        'justifyContent': 'space-between',
        'alignItems': 'center'
    }),

    # Main Content Area
    html.Div([
        # Left: Filters
        html.Div([
            html.Button("Clear Filters", id="clear_btn", style=filter_button_style),

            html.Label("Region", style=filter_label_style),
            dcc.Dropdown(id="region_dd", placeholder="Select Region(s)", multi=True,
                         style=dropdown_style),

            html.Label("Province", style=filter_label_style),
            dcc.Dropdown(id="province_dd", placeholder="Select Province(s)", multi=True,
                         style=dropdown_style),

            html.Label("Division", style=filter_label_style),
            dcc.Dropdown(id="division_dd", placeholder="Select Division(s)", multi=True,
                         style=dropdown_style),

            html.Label("District", style=filter_label_style),
            dcc.Dropdown(id="district_dd", placeholder="Select District(s)", multi=True,
                         style=dropdown_style),

            html.Label("Municipality", style=filter_label_style),
            dcc.Dropdown(id="municipality_dd", placeholder="Select Municipality(s)", multi=True,
                         style=dropdown_style),

            html.Label("Legislative District", style=filter_label_style),
            dcc.Dropdown(id="legislative_district_dd", placeholder="Select Legislative District(s)", multi=True,
                         style=dropdown_style),

            html.Label("Sector", style=filter_label_style),
            dcc.Dropdown(id="sector_dd", placeholder="Select Sector(s)", multi=True,
                         style=dropdown_style),

            html.Label("School Type", style=filter_label_style),
            dcc.Dropdown(id="school_type_dd", placeholder="Select School Type(s)", multi=True,
                         style=dropdown_style),

            html.Label("Modified COC", style=filter_label_style),
            dcc.Dropdown(id="modified_coc_dd", placeholder="Select Modified COC(s)", multi=True,
                         style=dropdown_style),

            html.Label("Subclass", style=filter_label_style),
            dcc.Dropdown(id="school_subclass_dd", placeholder="Select Subclass(s)", multi=True,
                         style=dropdown_style),
        ], style=filters_container_style),

        # Right: Metrics & Charts
        html.Div([
            # Top row metrics
            html.Div([
                html.Div([
                    html.Div(id="male_summary_card", style=male_number_style),
                    html.Div(style=metric_label_style)
                ], style=male_card_style),

                html.Div([
                    html.Div(id="female_summary_card", style=female_number_style),
                    html.Div(style=metric_label_style)
                ], style=female_card_style),

                html.Div([
                    html.Div(id="total_summary_card", style=total_enrollees_number_style),
                    html.Div(style=metric_label_style)
                ], style=total_enrollees_card_style),

                html.Div([
                    html.Div(id="total_school_card", style=total_schools_number_style),
                    html.Div(style=metric_label_style)
                ], style=total_schools_card_style),
            ], style={
                'display': 'flex',
                'gap': '15px',
                'marginBottom': '16px',
                'justifyContent': 'space-between',
                'width': '100%'
            }),

            # Wrap both charts in a flex container
            html.Div([
                html.Div([
                    html.H3("Educational Level Comparison", style=chart_heading_style),
                    dcc.Graph(
                        id="education_bar_chart",
                        style={"height": "250px", "width": "100%"},
                        config={'displayModeBar': False}
                    )
                ], style={**enrollment_chart_style, "flex": "1"}),

                html.Div([
                    html.H3("Average Student Count per Grade Level", style=chart_heading_style),
                    dcc.Graph(
                        id="enrollment_rate_chart",
                        style={"height": "250px", "width": "100%"},
                        config={'displayModeBar': False}
                    )
                ], style={**enrollment_chart_style, "flex": "1"}),

                html.Div([
                    html.H3("Average Student Count per Track", style=chart_heading_style),
                    dcc.Graph(
                        id="tracks_rate_chart",
                        style={"height": "250px", "width": "100%"},
                        config={'displayModeBar': False}
                    )
                ], style={**enrollment_chart_style, "flex": "1"}),

            ], style={"display": "flex", "gap": "15px"}),

            # School Level Charts in a row layout for better comparison
            html.Div([
                # Elementary Level
                html.Div([
                    html.H3("Elementary Level", style=chart_heading_style),
                    dcc.Graph(
                        id="elementary_bar_chart",
                        config={'displayModeBar': False},
                        style={"height": "250px", "width": "100%"}
                    )
                ], style={**enrollment_chart_style, "flex": "1"}),

                # Junior High School
                html.Div([
                    html.H3("Junior High School", style=chart_heading_style),
                    dcc.Graph(
                        id="jhs_bar_chart",
                        config={'displayModeBar': False},
                        style={"height": "250px", "width": "100%"}
                    )
                ], style={**enrollment_chart_style, "flex": "1"}),

                # Senior High School
                html.Div([
                    html.H3("Senior High School", style=chart_heading_style),
                    dcc.Graph(
                        id="shs_bar_chart",
                        config={'displayModeBar': False},
                        style={"height": "250px", "width": "100%"}
                    )
                ], style={**enrollment_chart_style, "flex": "1"}),
            ], style={'display': 'flex', "gap": "15px"})

        ], style={'flex': '1', 'width': '75%'}),
    ], style={'display': 'flex', 'gap': '15px', 'width': '100%'}),
], style={
    'width': '100%',
    'maxWidth': '1440px',
    'margin': '0 auto',
    'padding': '20px',
    'backgroundColor': COLORS['background'],
    'minHeight': '100vh',
    'fontFamily': 'Helvetica Neue, Arial, sans-serif',
    'boxSizing': 'border-box'
})

# Comparison Dashboard Layout
comparison_dashboard_layout = html.Section([

    # Store cleaned data
    dcc.Store(id='stored-data-present'),
    dcc.Store(id='stored-data-previous'),

    # Header with Logo
    html.Div([
        # Left side with logo and title
        html.Div([
            html.Img(
                src='https://upload.wikimedia.org/wikipedia/commons/f/fa/Seal_of_the_Department_of_Education_of_the_Philippines.png',
                style={'height': '100px', 'marginRight': '8px'}
            ),
            html.Div([
                html.H1("REPUBLIC OF THE PHILIPPINES",
                        style={'fontFamily': "'EB Garamond', serif", 'fontSize': '22px', 'margin': '0', 'marginBottom': '3px', 'fontWeight': '400'}),
                html.H2("DEPARTMENT OF EDUCATION",
                        style={'fontFamily': "'EB Garamond', serif", 'fontSize': '36px', 'margin': '0', 'fontWeight': '500'})
            ], style=header_text_style)
        ], style={'display': 'flex', 'alignItems': 'center'}),

        # Right side status
        html.Div(id='header-status', style={'color': COLORS['accent'], 'fontSize': '13px'}),
    ], style={
        **upper_header_style,
        'display': 'flex',
        'justifyContent': 'space-between',
        'alignItems': 'center'
    }),

    html.Div([
        html.H3("School Enrollment Dashboard",
                style={'fontFamily': 'Arial, sans-serif',
                       'color': COLORS['primary'],
                       'fontWeight': 'bold',
                       'fontSize': '40px',
                       'margin': '24px 0',
                       'marginLeft' : '20px',
                       'textAlign': 'left'})
    ]),

    # Upload Controls
    html.Div([
        html.Div([
            dcc.Upload(
                id='upload-data1',
                children=html.Button('Upload Present Year', style=primary_button_style),
                multiple=False,
                style={'marginRight': '10px'}
            ),
            dcc.Upload(
                id='upload-data2',
                children=html.Button('Upload Previous Year', style=primary_button_style),
                multiple=False,
                style={'marginRight': '10px'}
            ),
            html.Button(
                "Clear Files",
                id="clear-files-btn",
                style=danger_button_style
            )
        ], style={'display': 'flex', 'alignItems': 'center', "backgroundColor": 'white'}),

        # Upload Messages
        html.Div([
            html.Div(id='output-data1', style={'marginRight': '20px'}),
            html.Div(id='output-data2')
        ], style={'display': 'flex', 'alignItems': 'center', 'marginLeft': '20px'}),

        # Right side with back button
        dcc.Link(
            html.Button('Back to Main Dashboard', style={
                **button_style,
                'backgroundColor': COLORS['purple'],
                'color': 'white',
                'marginLeft': 'auto'  # Pushes to far right
            }),
            href='/'
        )
    ], style={
        **header_style,
        'display': 'flex',
        'justifyContent': 'space-between',
        'alignItems': 'center'
    }),

    # Main Content
    html.Div([
        # Left: Filters
        html.Div([
            html.Button(
                "Clear Filters",
                id="clear-filters-btn",
                style=filter_button_style
            ),

            html.Label("Region", style=filter_label_style),
            dcc.Dropdown(
                id='region-dropdown',
                placeholder='Select Region',
                multi=True,
                style=dropdown_style
            ),

            html.Label("Province", style=filter_label_style),
            dcc.Dropdown(
                id='province-dropdown',
                placeholder='Select Province',
                multi=True,
                style=dropdown_style
            ),

            html.Label("Division", style=filter_label_style),
            dcc.Dropdown(
                id='division-dropdown',
                placeholder='Select Division',
                multi=True,
                style=dropdown_style
            ),

            html.Label("District", style=filter_label_style),
            dcc.Dropdown(
                id='district-dropdown',
                placeholder='Select District',
                multi=True,
                style=dropdown_style
            ),

            html.Label("Municipality", style=filter_label_style),
            dcc.Dropdown(
                id='municipality-dropdown',
                placeholder='Select Municipality',
                multi=True,
                style=dropdown_style
            ),

            html.Label("Legislative District", style=filter_label_style),
            dcc.Dropdown(
                id='legislative-dropdown',
                placeholder='Select Legislative District',
                multi=True,
                style=dropdown_style
            ),

            html.Label("Sector", style=filter_label_style),
            dcc.Dropdown(
                id='sector-dropdown',
                placeholder='Select Sector',
                multi=True,
                style=dropdown_style
            ),

            html.Label("School Type", style=filter_label_style),
            dcc.Dropdown(
                id='school-type-dropdown',
                placeholder='Select School Type',
                multi=True,
                style=dropdown_style
            ),

            html.Label("Modified COC", style=filter_label_style),
            dcc.Dropdown(
                id='coc-dropdown',
                placeholder='Select Modified COC',
                multi=True,
                style=dropdown_style
            ),

            html.Label("Subclass", style=filter_label_style),
            dcc.Dropdown(
                id='subclass-dropdown',
                placeholder='Select Subclassification',
                multi=True,
                style=dropdown_style
            ),
        ], style=filters_container_style),

        # Right: Metrics & Charts
        html.Div([
            # Growth Card
            html.Div(id='growth-card', style={
                'backgroundColor': COLORS['white'],
                'padding': '16px 20px',
                'borderRadius': '12px',
                'marginBottom': '16px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.05)'
            }),

            # Overall Growth Chart
            html.Div([
                html.Div([
                    html.H3("Enrollment Growth", style=chart_heading_style),
                    dcc.Graph(
                        id='growth-chart',
                        config={'displayModeBar': False},
                        style={"height": "290px", "width": "100%"}
                    )
                ], style={**chart_style, "flex": "1"}),
            ], style={'display': 'flex', "gap": "15px"}),

            # Strand Comparison Charts
            html.Div([
                html.Div([
                    html.H3("SHS Strand Comparison", style=chart_heading_style),
                    dcc.Graph(
                        id='strand-chart',
                        config={'displayModeBar': False},
                        style={"height": "290px", "width": "100%"}
                    )
                ], style={**chart_style, "flex": "1"}),
            ], style={'display': 'flex', "gap": "15px"}),

            #Kinder to Grade 10 Comparison - Moved inside the right-side container
            html.Div([
                html.Div([
                    html.H3("Kinder to Grade 10 Comparison", style=chart_heading_style),
                    dcc.Graph(
                        id='k10-comparison-chart',
                        config={'displayModeBar': False},
                        style={"height": "290px", "width": "100%"}
                    )
                ], style={**chart_style, "flex": "1"}),
            ], style={'display': 'flex', "gap": "15px"}),

        ], style={'flex': '1', 'width': '75%'}), # Keep the flex and width for the right side
    ], style={'display': 'flex', 'gap': '15px', 'width': '100%'}),

], style={
    'width': '100%',
    'maxWidth': '1440px',
    'margin': '0 auto',
    'padding': '20px',
    'backgroundColor': COLORS['background'],
    'minHeight': '100vh',
    'fontFamily': 'Helvetica Neue, Arial, sans-serif',
    'boxSizing': 'border-box'
})

# =========================================================== END OF LAYOUTS =============================================================================

# =========================================================== HELPER FUNCTIONS ===========================================================================
def initial_dataset(contents):
    if contents is None:
        return pd.DataFrame()

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), skiprows=4)  # **EDIT HERE**
    except UnicodeDecodeError:
        df = pd.read_csv(io.StringIO(decoded.decode('latin-1')), skiprows=4)  # **EDIT HERE**

    df = df.fillna('Not Applicable')

    # Clean column names:
    df.columns = (
        df.columns
        .str.replace('-', '', regex=False)
        .str.replace(r'\s+', ' ', regex=True)
        .str.strip()
    )

    return df


def parse_contents(contents, filename):
    if contents is None:
        return pd.DataFrame()

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    try:
        if 'csv' in filename.lower():
            try:
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), skiprows=4)  # **EDIT HERE**
            except UnicodeDecodeError:
                df = pd.read_csv(io.StringIO(decoded.decode('latin-1')), skiprows=4)  # **EDIT HERE**
        elif 'xls' in filename.lower():
            df = pd.read_excel(io.BytesIO(decoded), skiprows=4)
        else:
            return pd.DataFrame()

        df = df.fillna('Not Applicable')
        df.columns = df.columns.str.replace('-', '', regex=False).str.replace(r'\s+', ' ', regex=True).str.strip()
        return df
    except Exception as e:
        print(f"Error parsing file: {str(e)}")
        return pd.DataFrame()


def get_active_df(present_data, previous_data):
    """Returns the most recent available dataframe"""
    if present_data:
        return pd.DataFrame(present_data)
    elif previous_data:
        return pd.DataFrame(previous_data)
    return pd.DataFrame()


def calculate_totals(df):
    """Calculate total enrollment from a dataframe"""
    if df.empty:
        return 0

    # Get all columns that contain Male/Female data
    gender_cols = [col for col in df.columns if 'Male' in col or 'Female' in col]
    return df[gender_cols].sum().sum()


def apply_filters(df, filters):
    """Apply all active filters to the dataframe"""
    if df.empty:
        return df

    for column, values in filters.items():
        if values:
            df = df[df[column].isin(values)]
    return df


# =========================================================== END OF HELPER FUNCTIONS ====================================================================

# =========================================================== CALLBACKS =================================================================================
# Page routing callback
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/comparison-dashboard':
        return comparison_dashboard_layout
    else:
        return main_dashboard_layout


# Main Dashboard Callbacks
@app.callback(
    Output('output-upload', 'children'),
    Output('stored-data', 'data'),
    Input('upload-dataset', 'contents'),
    Input('clear-btn', 'n_clicks'),
    State('upload-dataset', 'filename')
)
def handle_upload_or_clear(contents, clear_clicks, filename):
    triggered_id = ctx.triggered_id
    if triggered_id == 'clear-btn':
        return "Upload cleared. Please upload a new file.", None
    if contents is None:
        return "No file uploaded yet.", None

    try:
        df = initial_dataset(contents)
        return f"Uploaded: {filename}", df.to_dict('records')
    except Exception as e:
        return f"Error reading file: {e}", None


@app.callback(
    Output('region_dd', 'options'),
    Output('province_dd', 'options'),
    Output('division_dd', 'options'),
    Output('district_dd', 'options'),
    Output('municipality_dd', 'options'),
    Output('legislative_district_dd', 'options'),
    Output('sector_dd', 'options'),
    Output('school_type_dd', 'options'),
    Output('modified_coc_dd', 'options'),
    Output('school_subclass_dd', 'options'),
    Input('stored-data', 'data'),
    Input('region_dd', 'value'),
    Input('province_dd', 'value'),
    Input('division_dd', 'value'),
    Input('district_dd', 'value'),
    Input('municipality_dd', 'value'),
    Input('legislative_district_dd', 'value'),
    Input('sector_dd', 'value'),
    Input('school_type_dd', 'value'),
    Input('modified_coc_dd', 'value'),
)
def update_dropdown_options(data, region, province, division, district, municipality,
                            legislative_district, sector, school_type, modified_coc):
    if data is None:
        return ([],) * 10

    df = pd.DataFrame(data)

    # Region Options (use full data)
    region_options = [{'label': r, 'value': r} for r in sorted(df['Region'].dropna().unique())]

    # Province Options (filter only by region)
    province_df = df[df['Region'].isin(region)] if region else df
    province_options = [{'label': p, 'value': p} for p in sorted(province_df['Province'].dropna().unique())]

    # Division Options (filter by region and province)
    division_df = province_df[province_df['Province'].isin(province)] if province else province_df
    division_options = [{'label': d, 'value': d} for d in sorted(division_df['Division'].dropna().unique())]

    # District Options (filter by region, province, and district)
    district_df = division_df[division_df['Division'].isin(division)] if division else division_df
    district_options = [{'label': d, 'value': d} for d in sorted(district_df['District'].dropna().unique())]

    # Municipality Options (filter by region, province, district, division)
    municipality_df = district_df[district_df['District'].isin(district)] if district else district_df
    municipality_options = [{'label': m, 'value': m} for m in sorted(municipality_df['Municipality'].dropna().unique())]

    # Legislative District Options
    legislative_district_df = municipality_df[
        municipality_df['Municipality'].isin(municipality)] if municipality else municipality_df
    legislative_district_options = [{'label': l, 'value': l} for l in
                                    sorted(legislative_district_df['Legislative District'].dropna().unique())]

    # Sector Options
    sector_df = legislative_district_df[legislative_district_df['Legislative District'].isin(
        legislative_district)] if legislative_district else legislative_district_df
    sector_options = [{'label': s, 'value': s} for s in sorted(sector_df['Sector'].dropna().unique())]

    # School Type Options
    school_type_df = sector_df[sector_df['Sector'].isin(sector)] if sector else sector_df
    school_type_options = [{'label': s, 'value': s} for s in sorted(school_type_df['School Type'].dropna().unique())]

    # Modified COC Options
    modified_coc_df = school_type_df[school_type_df['School Type'].isin(school_type)] if school_type else school_type_df
    modified_coc_options = [{'label': m, 'value': m} for m in sorted(modified_coc_df['Modified COC'].dropna().unique())]

    # Subclass Options
    school_subclass_df = modified_coc_df[
        modified_coc_df['Modified COC'].isin(modified_coc)] if modified_coc else modified_coc_df
    school_subclass_options = [{'label': s, 'value': s} for s in
                               sorted(school_subclass_df['School Subclassification'].dropna().unique())]

    return (region_options, province_options, division_options, district_options,
            municipality_options, legislative_district_options, sector_options,
            school_type_options, modified_coc_options, school_subclass_options)


@app.callback(
    Output('region_dd', 'value'),
    Output('province_dd', 'value'),
    Output('division_dd', 'value'),
    Output('district_dd', 'value'),
    Output('municipality_dd', 'value'),
    Output('legislative_district_dd', 'value'),
    Output('sector_dd', 'value'),
    Output('school_type_dd', 'value'),
    Output('modified_coc_dd', 'value'),
    Output('school_subclass_dd', 'value'),
    Input('clear_btn', 'n_clicks'),
    prevent_initial_call=True
)
def clear_all_dropdowns(n_clicks):
    return ([],) * 10


@app.callback(
    Output('male_summary_card', 'children'),
    Output('female_summary_card', 'children'),
    Output('total_summary_card', 'children'),
    Output('total_school_card', 'children'),
    Output('education_bar_chart', 'figure'),
    Output('elementary_bar_chart', 'figure'),
    Output('jhs_bar_chart', 'figure'),
    Output('shs_bar_chart', 'figure'),
    Output('enrollment_rate_chart', 'figure'),
    Output('tracks_rate_chart', 'figure'),
    Input('stored-data', 'data'),
    Input('region_dd', 'value'),
    Input('province_dd', 'value'),
    Input('division_dd', 'value'),
    Input('district_dd', 'value'),
    Input('municipality_dd', 'value'),
    Input('legislative_district_dd', 'value'),
    Input('sector_dd', 'value'),
    Input('school_type_dd', 'value'),
    Input('modified_coc_dd', 'value'),
    Input('school_subclass_dd', 'value')
)
def update_metrics_and_chart(data, region, province, division, district, municipality,
                             legislative_district, sector, school_type, modified_coc, school_subclass):
    if data is None:
        empty_fig = px.bar(
            x=["Elementary", "Junior High School", "Senior High School"],
            y=[0, 0, 0],
            title="No data available",
            labels={"x": "Education Level", "y": "Enrollment"}
        )
        empty_fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font={'color': '#1d1d1f'},
            margin=dict(l=10, r=10, t=40, b=10),
            title_font_size=16,
            showlegend=False
        )
        return (
            html.Div(children=[html.Div("0", style={"font-size": "24px", "text-align": "center"}),
                               html.Div("Males",
                                        style={"font-size": "16px", "text-align": "center", "font-weight": "normal"})],
                     style={
                         "display": "flex", "flexDirection": "column", "alignItems": "center"}),
            html.Div(children=[html.Div("0", style={"font-size": "24px", "text-align": "center"}),
                               html.Div("Females",
                                        style={"font-size": "16px", "text-align": "center", "font-weight": "normal"})],
                     style={
                         "display": "flex", "flexDirection": "column", "alignItems": "center"}),
            html.Div(children=[html.Div("0", style={"font-size": "24px", "text-align": "center"}),
                               html.Div("Enrollment",
                                        style={"font-size": "16px", "text-align": "center", "font-weight": "normal"})],
                     style={
                         "display": "flex", "flexDirection": "column", "alignItems": "center"}),
            html.Div(children=[html.Div("0", style={"font-size": "24px", "text-align": "center"}),
                               html.Div("Schools",
                                        style={"font-size": "16px", "text-align": "center", "font-weight": "normal"})],
                     style={
                         "display": "flex", "flexDirection": "column", "alignItems": "center"}),
            empty_fig,
            empty_fig,
            empty_fig,
            empty_fig,
            empty_fig,
            empty_fig)

    df = pd.DataFrame(data)

    # this is fixed enrollees sum (will  not be changed based on the filters)
    enrollment_cols = [col for col in df.columns if 'Male' in col or 'Female' in col]
    df[enrollment_cols] = df[enrollment_cols].apply(pd.to_numeric, errors='coerce').fillna(0)
    fixed_enrollee_sum = int(df[enrollment_cols].sum().sum())

    # fixed total schools
    fixed_total_schools = df.drop_duplicates().shape[0]

    # Define columns
    elementary_male = ['K Male', 'G1 Male', 'G2 Male', 'G3 Male', 'G4 Male', 'G5 Male', 'G6 Male', 'Elem NG Male']
    elementary_female = ['K Female', 'G1 Female', 'G2 Female', 'G3 Female', 'G4 Female', 'G5 Female', 'G6 Female',
                         'Elem NG Female']
    junior_male = ['G7 Male', 'G8 Male', 'G9 Male', 'G10 Male', 'JHS NG Male']
    junior_female = ['G7 Female', 'G8 Female', 'G9 Female', 'G10 Female', 'JHS NG Female']
    senior_male = [
        'G11 ACAD ABM Male', 'G11 ACAD HUMSS Male', 'G11 ACAD STEM Male', 'G11 ACAD GAS Male', 'G11 ACAD PBM Male',
        'G11 TVL Male', 'G11 SPORTS Male', 'G11 ARTS Male', 'G12 ACAD ABM Male', 'G12 ACAD HUMSS Male',
        'G12 ACAD STEM Male', 'G12 ACAD GAS Male', 'G12 ACAD PBM Male', 'G12 TVL Male', 'G12 SPORTS Male',
        'G12 ARTS Male'
    ]
    senior_female = [
        'G11 ACAD ABM Female', 'G11 ACAD HUMSS Female', 'G11 ACAD STEM Female', 'G11 ACAD GAS Female',
        'G11 ACAD PBM Female',
        'G11 TVL Female', 'G11 SPORTS Female', 'G11 ARTS Female', 'G12 ACAD ABM Female', 'G12 ACAD HUMSS Female',
        'G12 ACAD STEM Female', 'G12 ACAD GAS Female', 'G12 ACAD PBM Female', 'G12 TVL Female', 'G12 SPORTS Female',
        'G12 ARTS Female'
    ]
    all_gender_cols = elementary_male + elementary_female + junior_male + junior_female + senior_male + senior_female

    # Apply filters
    filters = {
        'Region': region,
        'Province': province,
        'Division': division,
        'District': district,
        'Municipality': municipality,
        'Legislative District': legislative_district,
        'Sector': sector,
        'School Type': school_type,
        'Modified COC': modified_coc,
        'School Subclassification': school_subclass
    }

    for col, selected_values in filters.items():
        if selected_values:
            df = df[df[col].isin(selected_values)]

    df[all_gender_cols] = df[all_gender_cols].replace('Not Applicable', 0)
    df[all_gender_cols] = df[all_gender_cols].apply(pd.to_numeric, errors='coerce').fillna(0)

    total_male = df[[col for col in all_gender_cols if 'Male' in col]].sum().sum()
    total_female = df[[col for col in all_gender_cols if 'Female' in col]].sum().sum()
    total_enrollees = total_male + total_female
    total_schools = df['BEIS School ID'].nunique()

    # Apple-style plot formatting
    apple_theme = {
        'plot_bgcolor': 'white',
        'paper_bgcolor': 'white',
        'font': {'color': '#1d1d1f', 'family': 'SF Pro Display, Helvetica, Arial, sans-serif'},
        'title_font_size': 16,
        'xaxis': {'showgrid': False},
        'yaxis': {'showgrid': True, 'gridcolor': '#f5f5f7', 'title': None},
        'legend': {'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
        'margin': dict(l=10, r=10, t=40, b=10),
    }

    male_color = '#1582b5'
    female_color = '#f05374'

    # Education Level Bar Chart
    bar_data = pd.DataFrame({
        'Education Level': ['Elementary', 'Elementary', 'Junior High School', 'Junior High School',
                            'Senior High School', 'Senior High School'],
        'Gender': ['Male', 'Female'] * 3,
        'Enrollment': [
            df[elementary_male].sum().sum(), df[elementary_female].sum().sum(),
            df[junior_male].sum().sum(), df[junior_female].sum().sum(),
            df[senior_male].sum().sum(), df[senior_female].sum().sum()
        ]
    })

    # Calculate total enrollment per education level
    bar_data["Total Enrollment"] = bar_data.groupby("Education Level")["Enrollment"].transform("sum")

    bar_data["Education Level"] = bar_data["Education Level"].replace({
        "Junior High School": "Junior HS",
        "Senior High School": "Senior HS"
    })

    edu_order = ["Elementary", "Junior HS", "Senior HS"]

    education_fig = px.bar(
        bar_data,
        y="Enrollment",
        x="Education Level",
        color="Gender",
        barmode="stack",
        custom_data=["Total Enrollment", "Gender"],
        color_discrete_map={'Male': male_color, 'Female': female_color},
        category_orders={"Education Level": edu_order}
    )

    education_fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Gender: %{customdata[1]}<br>Enrollment: %{y}<br>Total Enrollment: %{customdata[0]:,}<extra></extra>"
    )

    education_fig.update_layout(**apple_theme)

    # Elementary

    grade_levels = ['K', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'Elem NG']
    male_values = [df[f'{lvl} Male'].sum() for lvl in grade_levels]
    female_values = [df[f'{lvl} Female'].sum() for lvl in grade_levels]
    total_values = [m + f for m, f in zip(male_values, female_values)]

    total_values_repeated = total_values * 2
    genders = ['Male'] * len(grade_levels) + ['Female'] * len(grade_levels)
    enrollments = male_values + female_values

    elementary_df = pd.DataFrame({
        'Grade Level': grade_levels * 2,
        'Gender': genders,
        'Enrollment': enrollments,
        'Total': total_values_repeated
    })

    elementary_fig = px.bar(
        elementary_df,
        x='Grade Level',
        y='Enrollment',
        color='Gender',
        barmode='stack',
        text='Enrollment',
        color_discrete_map={'Male': male_color, 'Female': female_color},
        custom_data=['Total', 'Gender'],
        category_orders={
            'Grade Level': ['K', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'Elem NG']
        },
        labels={'Grade Level': 'Grade Level'}
    )

    elementary_fig.update_layout(**apple_theme)

    elementary_fig.update_traces(
        texttemplate='%{text:,}',
        textposition='none',
        hovertemplate="<b>Grade Level: %{x}</b><br>Gender: %{customdata[1]}<br>Enrollment: %{y:,}<br>Total: %{customdata[0]:,}<extra></extra>"
    )

    elementary_fig.update_xaxes(
        tickmode='array',
        tickvals=grade_levels,
        ticktext=[lvl if lvl != 'Elem NG' else 'NG' for lvl in grade_levels]
    )

    # Junior HS
    jhs_levels = ['G7', 'G8', 'G9', 'G10', 'JHS NG']
    jhs_male_values = [df[f'{lvl} Male'].sum() for lvl in jhs_levels]
    jhs_female_values = [df[f'{lvl} Female'].sum() for lvl in jhs_levels]
    jhs_total_values = [m + f for m, f in zip(jhs_male_values, jhs_female_values)]

    jhs_total_repeated = jhs_total_values * 2
    jhs_genders = ['Male'] * len(jhs_levels) + ['Female'] * len(jhs_levels)
    jhs_enrollments = jhs_male_values + jhs_female_values

    jhs_df = pd.DataFrame({
        'Grade Level': jhs_levels * 2,
        'Gender': jhs_genders,
        'Enrollment': jhs_enrollments,
        'Total': jhs_total_repeated
    })

    jhs_fig = px.bar(
        jhs_df,
        x='Grade Level',
        y='Enrollment',
        color='Gender',
        barmode='stack',
        text='Enrollment',
        color_discrete_map={'Male': male_color, 'Female': female_color},
        custom_data=['Total', 'Gender'],
        category_orders={'Grade Level': ['G7', 'G8', 'G9', 'G10', 'JHS NG']}
    )

    jhs_fig.update_layout(**apple_theme)

    jhs_fig.update_traces(
        texttemplate='%{text:,}',
        textposition='none',
        hovertemplate="<b>Grade Level: %{x}</b><br>Gender: %{customdata[1]}<br>Enrollment: %{y:,}<br>Total: %{customdata[0]:,}<extra></extra>"
    )

    jhs_fig.update_xaxes(
        tickmode='array',
        tickvals=jhs_levels,
        ticktext=[lvl if lvl != 'JHS NG' else 'NG' for lvl in jhs_levels]
    )

    # Senior HS
    shs_tracks = [
        'ACAD ABM', 'ACAD HUMSS', 'ACAD STEM', 'ACAD GAS', 'ACAD PBM', 'TVL', 'SPORTS', 'ARTS'
    ]

    male_shs_values = [
        df[[f'G11 {track} Male' if 'G11' in f'G11 {track} Male' else f'G11 ACAD {track} Male',
            f'G12 {track} Male' if 'G12' in f'G12 {track} Male' else f'G12 ACAD {track} Male']].sum().sum()
        for track in shs_tracks
    ]
    female_shs_values = [
        df[[f'G11 {track} Female' if 'G11' in f'G11 {track} Female' else f'G11 ACAD {track} Female',
            f'G12 {track} Female' if 'G12' in f'G12 {track} Female' else f'G12 ACAD {track} Female']].sum().sum()
        for track in shs_tracks
    ]

    total_shs_values = [m + f for m, f in zip(male_shs_values, female_shs_values)]
    shs_total_repeated = total_shs_values * 2
    shs_genders = ['Male'] * len(shs_tracks) + ['Female'] * len(shs_tracks)
    shs_enrollments = male_shs_values + female_shs_values

    shs_df = pd.DataFrame({
        'Track': shs_tracks * 2,
        'Gender': shs_genders,
        'Enrollment': shs_enrollments,
        'Total': shs_total_repeated
    })

    shs_df['Track Cleaned'] = shs_df['Track'].str.replace('ACAD ', '', regex=False)

    shs_df = shs_df.sort_values('Total', ascending=False)

    shs_fig = px.bar(
        shs_df,
        orientation='h',
        x='Enrollment',
        y='Track Cleaned',
        color='Gender',
        barmode='stack',
        text='Enrollment',
        color_discrete_map={'Male': male_color, 'Female': female_color},
        custom_data=['Total', 'Gender']
    )

    shs_fig.update_layout(**apple_theme)

    shs_fig.update_layout(
        yaxis=dict(
            autorange='reversed'
        )
    )

    shs_fig.update_traces(
        texttemplate='%{text:,}',
        textposition='none',
        hovertemplate="<b>%{y}</b><br>Gender: %{customdata[1]}<br>Enrollment: %{x:,}<br>Total: %{customdata[0]:,}<extra></extra>"
    )

    # Student Count per Grade
    grade_levels = {
        'K': ['K Male', 'K Female'],
        'G1': ['G1 Male', 'G1 Female'],
        'G2': ['G2 Male', 'G2 Female'],
        'G3': ['G3 Male', 'G3 Female'],
        'G4': ['G4 Male', 'G4 Female'],
        'G5': ['G5 Male', 'G5 Female'],
        'G6': ['G6 Male', 'G6 Female'],
        'G7': ['G7 Male', 'G7 Female'],
        'G8': ['G8 Male', 'G8 Female'],
        'G9': ['G9 Male', 'G9 Female'],
        'G10': ['G10 Male', 'G10 Female'],
        'E-NG': ['Elem NG Male', 'Elem NG Female'],
        'J-NG': ['JHS NG Male', 'JHS NG Female']
    }

    data = []
    for level, cols in grade_levels.items():
        male_cols = [col for col in cols if 'Male' in col]
        female_cols = [col for col in cols if 'Female' in col]

        df[level + '_Male'] = df[male_cols].sum(axis=1)
        df[level + '_Female'] = df[female_cols].sum(axis=1)

        male_avg = round(df[level + '_Male'].mean())
        female_avg = round(df[level + '_Female'].mean())
        total_avg = male_avg + female_avg

        data.append(
            {'Grade Level': level, 'Gender': 'Male', 'Average Enrollees': male_avg, 'Total Enrollees': total_avg})
        data.append(
            {'Grade Level': level, 'Gender': 'Female', 'Average Enrollees': female_avg, 'Total Enrollees': total_avg})

    df_chart = pd.DataFrame(data)

    grade_order_map = {
        'K': 0,
        'G1': 1,
        'G2': 2,
        'G3': 3,
        'G4': 4,
        'G5': 5,
        'G6': 6,
        'G7': 7,
        'G8': 8,
        'G9': 9,
        'G10': 10,
        'E-NG': 11,
        'J-NG': 12
    }
    df_chart['Grade Order'] = df_chart['Grade Level'].map(grade_order_map)
    df_chart = df_chart.sort_values('Grade Order')

    df_chart = df_chart.sort_values('Grade Order')

    fig = px.bar(
        df_chart,
        x='Grade Level',
        y='Average Enrollees',
        color='Gender',
        barmode='stack',
        color_discrete_map={'Male': male_color, 'Female': female_color},
        custom_data=['Total Enrollees', 'Gender'],
    )

    fig.update_traces(
        hovertemplate=
        '<b>%{x}</b><br>' +
        'Gender: %{customdata[1]}<br>' +
        'Average Enrollees: %{y}<br>' +
        'Total Enrollees: %{customdata[0]}<br>' +
        '<extra></extra>'
    )

    fig.update_layout(**apple_theme)

    # Define SHS tracks
    shs_tracks = {
        'ABM': ['G11 ACAD ABM Male', 'G12 ACAD ABM Male', 'G11 ACAD ABM Female', 'G12 ACAD ABM Female'],
        'HUMSS': ['G11 ACAD HUMSS Male', 'G12 ACAD HUMSS Male', 'G11 ACAD HUMSS Female', 'G12 ACAD HUMSS Female'],
        'STEM': ['G11 ACAD STEM Male', 'G12 ACAD STEM Male', 'G11 ACAD STEM Female', 'G12 ACAD STEM Female'],
        'GAS': ['G11 ACAD GAS Male', 'G12 ACAD GAS Male', 'G11 ACAD GAS Female', 'G12 ACAD GAS Female'],
        'PBM': ['G11 ACAD PBM Male', 'G12 ACAD PBM Male', 'G11 ACAD PBM Female', 'G12 ACAD PBM Female'],
        'TVL': ['G11 TVL Male', 'G12 TVL Male', 'G11 TVL Female', 'G12 TVL Female'],
        'SPORTS': ['G11 SPORTS Male', 'G12 SPORTS Male', 'G11 SPORTS Female', 'G12 SPORTS Female'],
        'ARTS': ['G11 ARTS Male', 'G12 ARTS Male', 'G11 ARTS Female', 'G12 ARTS Female']
    }

    data = []
    for track, cols in shs_tracks.items():
        g11_male_col = [col for col in cols if 'G11' in col and 'Male' in col]
        g12_male_col = [col for col in cols if 'G12' in col and 'Male' in col]
        g11_female_col = [col for col in cols if 'G11' in col and 'Female' in col]
        g12_female_col = [col for col in cols if 'G12' in col and 'Female' in col]

        g11_male_avg = df[g11_male_col].mean(axis=1)
        g12_male_avg = df[g12_male_col].mean(axis=1)
        g11_female_avg = df[g11_female_col].mean(axis=1)
        g12_female_avg = df[g12_female_col].mean(axis=1)

        male_avg = round(((g11_male_avg + g12_male_avg) / 2).mean())
        female_avg = round(((g11_female_avg + g12_female_avg) / 2).mean())
        total_avg = male_avg + female_avg

        data.append({'Track': track, 'Gender': 'Male', 'Average Enrollees': male_avg, 'Total Enrollees': total_avg})
        data.append({'Track': track, 'Gender': 'Female', 'Average Enrollees': female_avg, 'Total Enrollees': total_avg})

    df_chart = pd.DataFrame(data)

    track_order = (
        df_chart.groupby('Track')['Total Enrollees']
        .sum()
        .sort_values(ascending=False)
        .index.tolist()
    )

    track_order = track_order[::-1]

    df_chart['Track'] = pd.Categorical(df_chart['Track'], categories=track_order, ordered=True)

    df_chart['Gender'] = pd.Categorical(df_chart['Gender'], categories=['Male', 'Female'], ordered=True)

    df_chart = df_chart.sort_values(by=['Track', 'Gender'], ascending=[True, True])

    # Plot
    fig_tracks = px.bar(
        df_chart,
        x='Average Enrollees',
        y='Track',
        color='Gender',
        barmode='stack',
        color_discrete_map={'Female': female_color, 'Male': male_color},
        custom_data=['Total Enrollees', 'Gender'],
    )

    fig_tracks.update_traces(
        hovertemplate=
        '<b>%{y}</b><br>' +
        'Gender: %{customdata[1]}<br>' +
        'Average Enrollees: %{x}<br>' +
        'Total Enrollees: %{customdata[0]}<br>' +
        '<extra></extra>'
    )

    fig_tracks.update_layout(**apple_theme)

    return (
        html.Div([
            html.H4("Male", style={'fontSize': '15px', 'margin': '0px', 'marginTop': '5px'}),
            html.Div(f"{int(total_male):,}", style={'fontSize': '30px', 'fontWeight': 'bold'}),
            html.Div(f"{int(total_male) / total_enrollees * 100:.1f}% of Total" if total_enrollees > 0 else "0%",
                     style={'fontSize': '14px', 'color': '#888'}), ]),

        html.Div([
            html.H4("Female", style={'fontSize': '15px', 'margin': '0px', 'marginTop': '5px'}),
            html.Div(f"{int(total_female):,}", style={'fontSize': '30px', 'fontWeight': 'bold'}),
            html.Div(f"{int(total_female) / total_enrollees * 100:.1f}% of Total" if total_enrollees > 0 else "0%",
                     style={'fontSize': '14px', 'color': '#888'}), ]),

        html.Div([
            html.H4("Enrollees", style={'fontSize': '15px', 'margin': '0px', 'marginTop': '5px'}),
            html.Div(f"{int(total_enrollees):,}", style={'fontSize': '30px', 'fontWeight': 'bold'}),
            html.Div(
                f"{int(total_enrollees) / fixed_enrollee_sum * 100:.1f}% of Nationwide" if fixed_enrollee_sum > 0 else "0%",
                style={'fontSize': '14px', 'color': '#888'}), ]),

        html.Div([
            html.H4("Schools", style={'fontSize': '15px', 'margin': '0px', 'marginTop': '5px'}),
            html.Div(f"{int(total_schools):,}", style={'fontSize': '30px', 'fontWeight': 'bold'}),
            html.Div(
                f"{int(total_schools) / fixed_total_schools * 100:.1f}% of Nationwide" if fixed_total_schools > 0 else "0%",
                style={'fontSize': '14px', 'color': '#888'}), ]),

        education_fig,
        elementary_fig,
        jhs_fig,
        shs_fig,
        fig,
        fig_tracks
    )


# Comparison Dashboard Callbacks
@app.callback(
    Output('header-status', 'children'),
    Input('stored-data-present', 'data'),
    Input('stored-data-previous', 'data')
)
def update_header_status(present_data, previous_data):
    if present_data and previous_data:
        return "Present & Previous Year Data Loaded"
    elif present_data:
        return "Present Year Data Loaded"
    elif previous_data:
        return "Previous Year Data Loaded"
    else:
        return "No Data Loaded"


@app.callback(
    Output('output-data1', 'children'),
    Output('output-data2', 'children'),
    Output('stored-data-present', 'data'),
    Output('stored-data-previous', 'data'),
    Input('upload-data1', 'contents'),
    Input('upload-data2', 'contents'),
    Input('clear-files-btn', 'n_clicks'),
    State('upload-data1', 'filename'),
    State('upload-data2', 'filename'),
    prevent_initial_call=True
)
def handle_file_uploads(contents1, contents2, clear_clicks, filename1, filename2):
    ctx = callback_context

    if not ctx.triggered:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == 'clear-files-btn':
        return "", "", None, None

    outputs = [dash.no_update, dash.no_update, dash.no_update, dash.no_update]

    if triggered_id == 'upload-data1' and contents1:
        df = parse_contents(contents1, filename1)
        if not df.empty:
            outputs[0] = f"{filename1} uploaded as present year"
            outputs[2] = df.to_dict('records')
        else:
            outputs[0] = f"Error reading {filename1}"

    if triggered_id == 'upload-data2' and contents2:
        df = parse_contents(contents2, filename2)
        if not df.empty:
            outputs[1] = f"{filename2} uploaded as previous year"
            outputs[3] = df.to_dict('records')
        else:
            outputs[1] = f"Error reading {filename2}"

    return tuple(outputs)


@app.callback(
    [Output(dd, 'value') for dd in [
        'region-dropdown', 'province-dropdown', 'division-dropdown', 'district-dropdown',
        'municipality-dropdown', 'legislative-dropdown', 'sector-dropdown',
        'school-type-dropdown', 'coc-dropdown', 'subclass-dropdown']
     ],
    Input('clear-filters-btn', 'n_clicks'),
    prevent_initial_call=True
)
def clear_filters(n):
    return [None] * 10

@app.callback(
    Output('region-dropdown', 'options'),
    Output('province-dropdown', 'options'),
    Output('division-dropdown', 'options'),
    Output('district-dropdown', 'options'),
    Output('municipality-dropdown', 'options'),
    Output('legislative-dropdown', 'options'),
    Output('sector-dropdown', 'options'),
    Output('school-type-dropdown', 'options'),
    Output('coc-dropdown', 'options'),
    Output('subclass-dropdown', 'options'),

    Input('stored-data-present', 'data'),
    Input('region-dropdown', 'value'),
    Input('province-dropdown', 'value'),
    Input('division-dropdown', 'value'),
    Input('district-dropdown', 'value'),
    Input('municipality-dropdown', 'value'),
    Input('legislative-dropdown', 'value'),
    Input('sector-dropdown', 'value'),
    Input('school-type-dropdown', 'value'),
    Input('coc-dropdown', 'value'),
)
def update_dropdowns(data, region, province, division, district, municipality,
                     legislative, sector, school_type, coc):

    if data is None:
        return ([],) * 10

    df = pd.DataFrame(data)

    # Region Options (use full data)
    region_options = [{'label': r, 'value': r} for r in sorted(df['Region'].dropna().unique())]

    # Province Options (filter only by region)
    province_df = df[df['Region'].isin(region)] if region else df
    province_options = [{'label': p, 'value': p} for p in sorted(province_df['Province'].dropna().unique())]

    # Division Options (filter by region and province)
    division_df = province_df[province_df['Province'].isin(province)] if province else province_df
    division_options = [{'label': d, 'value': d} for d in sorted(division_df['Division'].dropna().unique())]

    # District Options (filter by region, province, and district)
    district_df = division_df[division_df['Division'].isin(division)] if division else division_df
    district_options = [{'label': d, 'value': d} for d in sorted(district_df['District'].dropna().unique())]

    # Municipality Options (filter by region, province, district, division)
    municipality_df = district_df[district_df['District'].isin(district)] if district else district_df
    municipality_options = [{'label': m, 'value': m} for m in sorted(municipality_df['Municipality'].dropna().unique())]

    # Legislative District Options
    legislative_district_df = municipality_df[
        municipality_df['Municipality'].isin(municipality)] if municipality else municipality_df
    legislative_district_options = [{'label': l, 'value': l} for l in
                                    sorted(legislative_district_df['Legislative District'].dropna().unique())]

    # Sector Options
    sector_df = legislative_district_df[legislative_district_df['Legislative District'].isin(legislative)] if legislative else legislative_district_df
    sector_options = [{'label': s, 'value': s} for s in sorted(sector_df['Sector'].dropna().unique())]

    # School Type Options
    school_type_df = sector_df[sector_df['Sector'].isin(sector)] if sector else sector_df
    school_type_options = [{'label': s, 'value': s} for s in sorted(school_type_df['School Type'].dropna().unique())]

    # Modified COC Options
    modified_coc_df = school_type_df[school_type_df['School Type'].isin(school_type)] if school_type else school_type_df
    modified_coc_options = [{'label': m, 'value': m} for m in sorted(modified_coc_df['Modified COC'].dropna().unique())]

    # Subclass Options
    school_subclass_df = modified_coc_df[modified_coc_df['Modified COC'].isin(coc)] if coc else modified_coc_df
    school_subclass_options = [{'label': s, 'value': s} for s in sorted(school_subclass_df['School Subclassification'].dropna().unique())]

    return (region_options, province_options, division_options, district_options,
            municipality_options, legislative_district_options, sector_options,
            school_type_options, modified_coc_options, school_subclass_options)


@app.callback(
    Output('growth-card', 'children'),
    Output('growth-chart', 'figure'),
    Output('strand-chart', 'figure'),
    Output('k10-comparison-chart', 'figure'),

    Input('stored-data-present', 'data'),
    Input('stored-data-previous', 'data'),
    Input('region-dropdown', 'value'),
    Input('province-dropdown', 'value'),
    Input('division-dropdown', 'value'),
    Input('district-dropdown', 'value'),
    Input('municipality-dropdown', 'value'),
    Input('legislative-dropdown', 'value'),
    Input('sector-dropdown', 'value'),
    Input('school-type-dropdown', 'value'),
    Input('coc-dropdown', 'value'),
    Input('subclass-dropdown', 'value')
)
def update_growth_card(present_data, previous_data, region, province, district, division,
                       municipality, legislative, sector, school_type, coc, subclass):
    # Create empty figures for the case when data is not available
    empty_figure = px.bar(title="No data available")

    if not present_data or not previous_data:
        # Return a tuple with placeholders for all outputs
        return (
            html.Div("Upload both present and previous year data to see growth comparison",
                     style={'textAlign': 'center', 'color': COLORS['accent']}),
            empty_figure,  # Empty figure for growth chart
            empty_figure,  # Empty figure for strand chart
            empty_figure   # Empty figure for k10 comparison chart
        )

    # Convert stored data back to DataFrames
    df_present = pd.DataFrame(present_data)
    df_previous = pd.DataFrame(previous_data)

    # Apply filters - create a dictionary of filters to apply
    filters = {
        'Region': region,
        'Province': province,
        'District': district,
        'Division': division,
        'Municipality': municipality,
        'Legislative District': legislative,
        'Sector': sector,
        'School Type': school_type,
        'Modified COC': coc,
        'School Subclassification': subclass
    }

    # Apply filters to both present and previous year data
    filtered_present = apply_filters(df_present, filters)
    filtered_previous = apply_filters(df_previous, filters)

    # Check if filtered data is empty after applying filters
    if filtered_present.empty or filtered_previous.empty:
        return (
            html.Div("No data available for the selected filters",
                     style={'textAlign': 'center', 'color': COLORS['accent']}),
            empty_figure,
            empty_figure,
            empty_figure
        )

    # Calculate totals for growth card
    total_present = calculate_totals(filtered_present)
    total_previous = calculate_totals(filtered_previous)

    # Calculate growth
    difference = total_present - total_previous
    percent_change = (difference / total_previous * 100) if total_previous != 0 else 0

    # Determine color and arrow based on growth/decline
    if difference > 0:
        color = COLORS['success']
        arrow = '↑'
    elif difference < 0:
        color = COLORS['error']
        arrow = '↓'
    else:
        color = COLORS['accent']
        arrow = '→'

    # Helper function to compute totals for each education level
    def compute_totals(df, level_prefixes):
        total = 0
        for prefix in level_prefixes:
            male_cols = [col for col in df.columns if prefix in col and 'Male' in col]
            female_cols = [col for col in df.columns if prefix in col and 'Female' in col]

            # Only sum columns that actually exist in the dataframe
            valid_cols = [col for col in male_cols + female_cols if col in df.columns]
            if valid_cols:
                total += df[valid_cols].sum().sum()
        return total

    # Define level prefixes for grouping
    levels = {
        'Elementary': ['K ', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6'],
        'JHS': ['G7', 'G8', 'G9', 'G10'],
        'SHS': ['G11', 'G12']
    }

    # Create data for enrollment trend chart
    trend_data = []
    for label, prefixes in levels.items():
        prev_total = compute_totals(filtered_previous, prefixes)
        curr_total = compute_totals(filtered_present, prefixes)
        dropout = max(prev_total - curr_total, 0)
        dropout_rate = dropout / prev_total * 100 if prev_total else 0
        trend_data.append({
            'Level': label,
            'Previous Year': prev_total,
            'Present Year': curr_total,
            'Dropouts': dropout,
            'Dropout Rate (%)': dropout_rate
        })

    # Convert to DataFrame for charting
    trend_df = pd.DataFrame(trend_data)

    # Set colors for current and previous years
    present_color = '#199ad6'
    previous_color = '#ff375f'
    # Create enrollment comparison chart
    enroll_fig = px.bar(trend_df, x='Level', y=['Previous Year', 'Present Year'], labels={'value': 'Number of Students', 'variable': 'Year'},
                        barmode='group', color='variable', color_discrete_map={'Previous Year': previous_color, 'Present Year': present_color})

    enroll_fig.update_layout(
        {
    'plot_bgcolor': 'white',
    'paper_bgcolor': 'white',
    'font': {'color': '#1d1d1f', 'family': 'SF Pro Display, Helvetica, Arial, sans-serif'},
    'title_font_size': 16,
    'xaxis': {'showgrid': False},
    'yaxis': {'showgrid': True, 'gridcolor': '#f5f5f7', 'title': None},
    'legend': {'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
    'margin': dict(l=10, r=10, t=40, b=10),
})

    # ===== SHS STRAND COMPARISON =====
    strands = ['ABM', 'HUMSS', 'STEM', 'GAS', 'PBM', 'TVL', 'SPORTS', 'ARTS']
    strand_map = {
        'ABM': ['G11 ACAD ABM Male', 'G11 ACAD ABM Female', 'G12 ACAD ABM Male', 'G12 ACAD ABM Female'],
        'HUMSS': ['G11 ACAD HUMSS Male', 'G11 ACAD HUMSS Female', 'G12 ACAD HUMSS Male',
                  'G12 ACAD HUMSS Female'],
        'STEM': ['G11 ACAD STEM Male', 'G11 ACAD STEM Female', 'G12 ACAD STEM Male', 'G12 ACAD STEM Female'],
        'GAS': ['G11 ACAD GAS Male', 'G11 ACAD GAS Female', 'G12 ACAD GAS Male', 'G12 ACAD GAS Female'],
        'PBM': ['G11 ACAD PBM Male', 'G11 ACAD PBM Female', 'G12 ACAD PBM Male', 'G12 ACAD PBM Female'],
        'TVL': ['G11 TVL Male', 'G11 TVL Female', 'G12 TVL Male', 'G12 TVL Female'],
        'SPORTS': ['G11 SPORTS Male', 'G11 SPORTS Female', 'G12 SPORTS Male', 'G12 SPORTS Female'],
        'ARTS': ['G11 ARTS Male', 'G11 ARTS Female', 'G12 ARTS Male', 'G12 ARTS Female']
    }

    # Calculate strand totals using filtered data
    df1_totals = {}
    for s in strands:
        cols = [col for col in strand_map[s] if col in filtered_present.columns]
        df1_totals[s] = filtered_present[cols].sum().sum() if cols else 0

    df2_totals = {}
    for s in strands:
        cols = [col for col in strand_map[s] if col in filtered_previous.columns]
        df2_totals[s] = filtered_previous[cols].sum().sum() if cols else 0

    # Create DataFrame for strand comparison
    comparison_df = pd.DataFrame({
        'Strand': strands,
        'Previous Year': [df2_totals[s] for s in strands],
        'Present Year': [df1_totals[s] for s in strands]

    })

    # Create strand comparison chart
    strand_comparison_fig = px.bar(
        comparison_df.melt(id_vars='Strand'),
        x='Strand', y='value', color='variable',
        labels={'value': 'Number of Students', 'variable': 'Year'},
        barmode='group',
        color_discrete_map={'Present Year': present_color, 'Previous Year': previous_color}
    )

    # Apply custom layout and theme
    apple_theme = {
    'plot_bgcolor': 'white',
    'paper_bgcolor': 'white',
    'font': {'color': '#1d1d1f', 'family': 'SF Pro Display, Helvetica, Arial, sans-serif'},
    'title_font_size': 16,
    'xaxis': {'showgrid': False},
    'yaxis': {'showgrid': True, 'gridcolor': '#f5f5f7', 'title': None},
    'legend': {'orientation': 'h', 'yanchor': 'bottom', 'y': 1.02, 'xanchor': 'right', 'x': 1},
    'margin': dict(l=10, r=10, t=40, b=10),
}
    strand_comparison_fig.update_layout(
        **apple_theme)

    # ===== KINDER TO GRADE 10 COMPARISON =====
    grade_levels = ['K', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'Elem NG']
    jhs_levels = ['G7', 'G8', 'G9', 'G10', 'JHS NG']
    all_levels = grade_levels + jhs_levels

    # Create dictionaries to map grade levels to their respective columns
    grade_level_map = {level: [f'{level} Male', f'{level} Female'] for level in all_levels}

    # Calculate K10 totals using filtered data
    df1_k10_totals = {}
    df2_k10_totals = {}

    for level in all_levels:
        cols = [col for col in grade_level_map[level] if col in filtered_present.columns]
        df1_k10_totals[level] = filtered_present[cols].sum().sum() if cols else 0

        cols = [col for col in grade_level_map[level] if col in filtered_previous.columns]
        df2_k10_totals[level] = filtered_previous[cols].sum().sum() if cols else 0

    # Create DataFrame for K10 comparison
    k10_comparison_df = pd.DataFrame({
        'Grade Level': all_levels,
        'Previous Year': [df2_k10_totals.get(level, 0) for level in all_levels],
        'Present Year': [df1_k10_totals.get(level, 0) for level in all_levels]
    })

    # Create K10 comparison chart
    k10_comparison_fig = px.bar(
        k10_comparison_df.melt(id_vars='Grade Level'),
        x='Grade Level', y='value', color='variable',
        labels={'value': 'Number of Students', 'variable': 'Year'},
        color_discrete_map={'Previous Year': previous_color, 'Present Year': present_color, },
        barmode='group'
    )

    k10_comparison_fig.update_layout(
        **apple_theme)

    # Create growth card display
    growth_card = html.Div([
        html.Div([
            # Previous Year
            html.Div([
                html.Div("Previous Year", style={'fontSize': '14px', 'color': COLORS['accent'], 'textAlign': 'center'}),
                html.Div(f"{int(total_previous):,}", style={
                    'fontSize': '24px',
                    'fontWeight': 'bold',
                    'textAlign': 'center',
                    'margin': '5px 0'
                })
            ], style={'flex': 1, 'padding': '10px'}),

            # Present Year
            html.Div([
                html.Div("Present Year", style={'fontSize': '14px', 'color': COLORS['accent'], 'textAlign': 'center'}),
                html.Div(f"{int(total_present):,}", style={
                    'fontSize': '24px',
                    'fontWeight': 'bold',
                    'textAlign': 'center',
                    'margin': '5px 0'
                })
            ], style={'flex': 1, 'padding': '10px', 'borderLeft': '1px solid #d2d2d7',
                      'borderRight': '1px solid #d2d2d7'}),

            # Change
            html.Div([
                html.Div("Change", style={'fontSize': '14px', 'color': COLORS['accent'], 'textAlign': 'center'}),
                html.Div([
                    html.Span(f"{arrow} {abs(int(difference)):,}", style={
                        'color': color,
                        'fontSize': '24px',
                        'fontWeight': 'bold',
                        'marginRight': '5px'
                    }),
                    html.Span(f"({percent_change:.1f}%)", style={
                        'color': color,
                        'fontSize': '18px'
                    })
                ], style={'textAlign': 'center', 'margin': '5px 0'})
            ], style={'flex': 1, 'padding': '10px'})
        ], style={
            'display': 'flex',
            'justifyContent': 'space-around',
            'alignItems': 'center'
        })
    ])

    # Return all four outputs as a tuple
    return growth_card, enroll_fig, strand_comparison_fig, k10_comparison_fig
if __name__ == '__main__':
    app.run(debug=True)