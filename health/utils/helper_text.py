from htmltools import TagList, tags
from shiny.ui import modal, modal_button, modal_show

about_funds = TagList(
    tags.h3("Funding and Impact Analysis"),
    tags.br(),
    tags.p(
        """
        We highlight insights from an analysis of the dynamics of Horizon Europe research investment and its contributions to Health.
        """,
        style="""
        text-align: justify;
        word-break:break-word;
        hyphens: auto;
        """,
    ),
)


about_graph = TagList(
    tags.h3("Network Analysis"),
    tags.br(),
    tags.p(
        """
        Using NetworkX, we identify collaboration patterns at country- and organization-level and relate its to publication outputs.        
        """,
        style="""
        text-align: justify;
        word-break:break-word;
        hyphens: auto;
        """,
    ),
)


about_topic = TagList(
    tags.h3("Thematic Analysis"),
    tags.br(),
    tags.p(
        """
        Using the BERTopic framework, we delve into health projects' description to identify emerging topics, trends, funding, and publication patterns.        
        """,
        style="""
        text-align: justify;
        word-break:break-word;
        hyphens: auto;
        """,
    ),
)



slider_text_map = tags.p(
    """
    Please use the slider below to choose the year. The map will
    reflect data for the input
    """,
    style="""
    text-align: justify;
    word-break:break-word;
    hyphens: auto;
    """,
)

slider_text_plot = tags.p(
    """
    Please use the dropdown to select the countries to compare. By default, the data for all countries are plotted.
    """,
    style="""
    text-align: justify;
    word-break:break-word;
    hyphens: auto;
    """,
)

dataset_information = TagList(
    tags.strong(tags.h3("Dataset Information")),
    tags.p(
        """
        We use multiple data sets from the Horizon Europe CORDIS database, which includes details about 15,341 projects between 2021-2027.
        Additionally, we obtain data on gross domestic product per capita (GDP) and healthy life years at birth (HLY) from EUROSTAT.
        References
        to all three can be found below.
        """,
        style="""
        text-align: justify;
        word-break:break-word;
        hyphens: auto;
        """,
    ),
    tags.ul(
        tags.li(
            tags.a(
                "CORDIS",
                href=(
                    "https://data.europa.eu/data/datasets/cordis-eu-research-projects-under-horizon-europe-2021-2027?locale=en"
                ),
            )
        ),
        tags.li(
            tags.a(
                "GDP",
                href=(
                    "https://ec.europa.eu/eurostat/databrowser/view/nama_10_pc/default/table?lang=en"
                ),
            )
        ),
        tags.li(
            tags.a(
                "HLY",
                href=(
                    "https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Healthy_life_years_statistics"
                ),
            )
        ),
    ),
)

missing_note = TagList(
    tags.p(
        tags.strong("Note: "),
        """
        CORDIS datasets are produced monthly. Therefore, inconsistencies may occur between what is presented on the CORDIS live website and the datasets.
        """,
        style="""
        font-size: 14px;
        text-align: justify;
        word-break:break-word;
        hyphens: auto;
        """,
    ),
)


def info_modal():
    modal_show(
        modal(
            tags.strong(tags.h3("Unpacking Horizon Europe contributions to Health")),
            tags.p("An NLP-based analysis of the Horizon Europe R&D&I programmes"),
            tags.hr(),
            tags.strong(tags.h4("Problem Statement")),
            tags.p(
                """
            The publicly available Horizon Europe CORDIS dataset provides a vast amount of information on research and innovations across Europe, 
            but the sheer volume and diversity of data present unique challenges in understanding its dynamics and extracting meaningful insights. 
            One key thematic area of investment is Health, organized in Cluster 1 of Horizon Europe, and is the focus of our project.
            
            Advances in Natural Language Processing (NLP) and text mining offer a powerful opportunity to bridge this gap by systematically 
            exploring these open-access resources for knowledge extraction and thematic organization. Through a combination of computational methods, 
            data visualization, and cross-dataset comparisons, we aim to analyze the dynamics of Horizon Europe research investment and its contributions to Health.
            """,
                style="""
            text-align: justify;
            word-break:break-word;
            hyphens: auto;
            """,
            ),
            tags.hr(),
            dataset_information,
            tags.hr(),
            missing_note,
            size="l",
            easy_close=True,
            footer=modal_button("Close"),
        )
    )
