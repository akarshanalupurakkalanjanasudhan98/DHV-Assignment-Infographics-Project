# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 11:16:44 2024

@author: ACER
"""

import csv
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.gridspec import GridSpec as gsp
from matplotlib.gridspec import GridSpec


def read_data(file_path):
    # Read data from CSV file
    with open(file_path, 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        # Return the entire data
        return list(csv_reader)


def plot_stacked_bar_visualization(data, indicator_to_plot, selected_years, countries_to_plot, ax=None):
    # If ax is not provided, create a new plot
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 8))

    # Create a dictionary to store data for each country and year
    country_year_data = {country: {year: 0 for year in selected_years}
                         for country in countries_to_plot}

    # Extract data for the chosen indicator and years
    for row in data:
        if row['Indicator Name'] == indicator_to_plot and int(row['Year']) in selected_years:
            year = int(row['Year'])
            for country in countries_to_plot:
                country_year_data[country][year] += float(row[country])

    # Plot the data as a stacked bar chart
    bar_width = 0.8  # Adjust the width of the bars

    # Define the positions for each bar
    positions = np.arange(len(countries_to_plot))

    for i, year in enumerate(selected_years):
        # Adjust the positions for each year
        year_positions = positions
        values = np.array([country_year_data[country][year]
                          for country in countries_to_plot])

        # Bottom parameter ensures stacking
        ax.bar(year_positions, values, width=bar_width, label=str(
            year), alpha=0.8, edgecolor='w', linewidth=0.5)

    # Add labels and title
    ax.set_xlabel('Country')
    ax.set_ylabel('Value')
    ax.set_title(
        'Stacked Bar Plot for {} (from 1990 to 2010)'.format(indicator_to_plot))

    # Set x-axis ticks and labels
    ax.set_xticks(positions)
    ax.set_xticklabels(countries_to_plot)

    # Add legend
    ax.legend(title='Year')

    # If ax was not provided, show the plot
    if not ax:
        plt.show()

    # Return the axis for potential further customization
    return ax


def plot_3d_linegraph(data, indicator_to_plot, start_year, end_year, countries_to_plot, ax=None):
    # If ax is not provided, create a new 3D plot
    if ax is None:
        fig = plt.figure(figsize=(10, 6), facecolor="gold")
        ax = fig.add_subplot(111, projection='3d')

    # Create a dictionary to store data for each country
    country_data = {country: {'years': [], 'data': []}
                    for country in countries_to_plot}

    # Extract years and data for the chosen indicator within the specified range
    for i, row in enumerate(data):
        if row['Indicator Name'] == indicator_to_plot and start_year <= int(row['Year']) <= end_year:
            for j, country in enumerate(countries_to_plot):
                country_data[country]['years'].append(int(row['Year']))
                # Assuming the column for the country is the same as the country name
                value = float(row[country])
                country_data[country]['data'].append(value)

    # Plot the data for each country in 3D space
    for j, country in enumerate(countries_to_plot):
        ax.plot(country_data[country]['years'], [j]*len(country_data[country]['years']),
                country_data[country]['data'], label=f'{country}', linewidth=2, marker='o', markersize=5)

    # Add labels and title
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Country Index', fontsize=12)
    # Set z-label with extra padding
    ax.set_zlabel('Value', labelpad=20, fontsize=12)
    ax.set_title('3D Line Plot for {}'.format(indicator_to_plot), fontsize=14)

    # Add legend to the right side
    ax.legend(loc='upper left', bbox_to_anchor=(1, 0.5), fontsize=10)

    # Customize grid lines
    ax.grid(True, linestyle='--', alpha=0.7)

    # Customize ticks
    ax.tick_params(axis='both', which='major', labelsize=10)

    # If ax was not provided, show the plot
    if not ax:
        plt.show()

    # Return the axis for potential further customization
    return ax


def pie_chart_visualization(data, indicator_to_plot, year, ax=None, explode=None):
    # If ax is not provided, create a new plot
    if ax is None:
        fig, ax = plt.subplots()

    # Create a dictionary to store data for each country
    country_data = {}

    # Extract data for the chosen indicator and year
    for row in data:
        if row['Indicator Name'] == indicator_to_plot and int(row['Year']) == year:
            for country in row.keys():
                if country != 'Year' and country != 'Indicator Name' and row[country] != '':
                    country_data[country] = float(row[country])

    # Print the data used for the plot

    lighter_colors = ['#add8e6', '#ffb366', '#b3ffb3', '#ffb3b3', '#c2c2f0']

    # Extract values and labels from the dictionary
    labels = list(country_data.keys())
    values = list(country_data.values())

    # Find the index of the largest value
    max_index = values.index(max(values))

    # Explode slices if specified, with emphasis on the largest wedge
    explode = [
        0.1 if i == max_index and explode is None else 0 for i in range(len(labels))]

    # Plot the data as a pie chart with additional styles
    wedges, texts, autotexts = ax.pie(values, labels=labels, colors=lighter_colors, autopct='%1.1f%%', startangle=90,
                                      explode=explode, textprops={'fontsize': 10, 'fontweight': 'bold'})

    # Add a shadow effect to create a 3D appearance
    for i, wedge in enumerate(wedges):
        if i == max_index:
            wedge.set_edgecolor('gray')
            wedge.set_linewidth(1.5)  # Increase the linewidth for emphasis
        else:
            wedge.set_edgecolor('gray')
            wedge.set_linewidth(1)

    # Equal aspect ratio ensures that the pie chart is circular
    ax.axis('equal')

    # Add title
    ax.set_title('Pie Chart for {} in {}'.format(
        indicator_to_plot, year))

    # If ax was not provided, show the plot
    if not ax:
        plt.show()

    # Return the axis for potential further customization
    return ax


def area_plot_visualization(data, indicator_to_plot, start_year, end_year, countries_to_plot, ax=None):
    # If ax is not provided, create a new plot
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 8))

    # Filter data for the chosen indicator and years
    filtered_data = [row for row in data if row['Indicator Name'] ==
                     indicator_to_plot and start_year <= int(row['Year']) <= end_year]

    # Create a dictionary to store data for each source
    sources_data = {source: {'years': [], 'data': []} for source in data[0].keys(
    ) if source not in ['Year', 'Indicator Name'] and source in countries_to_plot}

    # Extract years and data for each source
    for row in filtered_data:
        for source in sources_data.keys():
            sources_data[source]['years'].append(int(row['Year']))
            sources_data[source]['data'].append(float(row[source]))

    # Create a list of years
    years = list(set(year for source_data in sources_data.values()
                 for year in source_data['years']))

    # Plot the data as a stacked area plot
    ax.stackplot(years,
                 *[sources_data[c]['data'] for c in countries_to_plot],
                 labels=countries_to_plot)

    # Add labels and title
    ax.set_xlabel('Year')
    ax.set_ylabel('Percentage of Total')
    ax.set_title(
        f'Stacked Area Plot for {indicator_to_plot} ({start_year} to {end_year})')

    # Add legend
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

    # If ax was not provided, show the plot
    if not ax:
        plt.show()

    # Return the axis for potential further customization
    return ax


def create_dashboard(data, countries):
    # Create a 2x2 grid for subplots
    fig = plt.figure(figsize=(20, 20), facecolor='#D2B48C')
    fig.text(0.5, 0.92, "Name: Akarsha Nalupurakkal Anjanasudhan        StudentId: 22078150",
             ha="center", fontweight='bold', fontsize=15)

    gs = GridSpec(2, 2, hspace=0.4, wspace=0.4)

    # First Plot (Stacked Bar Plot)
    ax1 = fig.add_subplot(gs[0, 0])
    plot_stacked_bar_visualization(data, 'CO2 emissions from solid fuel consumption (% of total)', [
                                   1991, 1993, 1995, 1997, 1999, 2003], countries, ax=ax1)
    ax1.set_title(
        'Stacked Bar Plot: CO2 emissions from solid fuel consumption (1991-2003)')
    ax1.text(0.5, -0.15, """India experienced fluctuating solid fuel emissions from 1991 to 2003, peaking at 73.43% in 1993. \n Canada's emissions remained relatively stable, ranging from 21.06% to 23.74%. 
    Germany witnessed a gradual decline, from 47.81% in 1991 to 39.25% in 2003.\n The United Kingdom showed a declining trend, reaching 24.93% in 1999. 
   Switzerland had minimal emissions, ranging from 0.81% to 2.52%. \n Overall, each country had distinct patterns in CO2 emissions from solid fuel consumption during this period.""",
             ha='center', va='center', transform=ax1.transAxes, fontsize=12, color='black')

    # Second Plot (3D Line Plot)
    ax2 = fig.add_subplot(gs[0, 1], projection='3d')
    plot_3d_linegraph(
        data, 'CO2 emissions from liquid fuel consumption (% of total)', 1991, 2003, countries, ax=ax2)
    ax2.set_title(
        '3D Line Plot: CO2 emissions from liquid fuel consumption (1991-2003)')
    ax2.text2D(0.5, -0.15, """ India's CO2 emissions from liquid fuel rose from 27.4% (1991) to 31.6% (1999), fluctuating. 
               Canada stabilized from 46.6% (1991) to 45.7% (1995), gradually rising. Germany increased to 38.9% (1999). 
               The UK fluctuated around 39.3%. Switzerland declined from 76.7% (1991) to 71.1% (2003).""",
               ha='center', va='center', transform=ax2.transAxes, fontsize=12, color='black')

    # Third Plot (Pie Chart)
    ax3 = fig.add_subplot(gs[1, 0])
    pie_chart_visualization(
        data, 'CO2 emissions from gaseous fuel consumption (% of total)', 2002, ax=ax3)
    ax3.set_title(
        'Pie Chart: CO2 emissions from gaseous fuel consumption (2002)')
    ax3.text(0.5, -0.15, """In 2002, United Kingdom had the highest contribution (37.08%) to CO2 emissions from gaseous fuel consumption 
        among the countries, while India had the lowest contribution (4.78%). Canada, Germany, and Switzerland 
        had intermediate contributions of 31.97%, 20.77%, and 13.07%, respectively.
             """,
             ha='center', va='center', transform=ax3.transAxes, fontsize=12, color='black')

    # set fourth grid point - Stacked Area Plot
    ax4 = fig.add_subplot(gs[1, 1])
    area_plot_visualization(
        data, 'CO2 emissions from gaseous fuel consumption (% of total)', 1991, 2003, countries, ax=ax4)

    ax4.set_title(
        'Area Plot : CO2 emissions from gaseous fuel consumption (% of total) from 1992 to 2002')
    ax4.text(0.5, -0.15, """In India, there was a steady decrease from 3.88% in 1991 to 4.92% in 2003.
                            Canada's emissions fluctuated within the range of 31-34%, reaching a peak in 2002.
                            Germany exhibited a relatively stable pattern, maintaining emissions between 14-20%. 
                            The United Kingdom experienced a gradual increase from 20.43% in 1991 to 37.08% in 2002,
                            followed by a slight decrease. Switzerland maintained emissions in the range of 9-13%, 
                            showing consistent levels with some fluctuations """,
             ha='center', va='center', transform=ax4.transAxes, fontsize=12, color='black')
    ax4.set_xlabel('')
    ax4.set_ylabel('')

    conclusion_text = """\n Description:
    This dashboard provides insights The stacked bar plot reveals fluctuating solid fuel emissions in India from 1991 to 2003,
    peaking at 73.43% in 1993, while Canada remained stable (21.06-23.74%). Germany showed a gradual decline, from 47.81% in 1991 to 39.25% in 2003.
    The UK displayed a declining trend, reaching 24.93% in 1999, and Switzerland had minimal emissions (0.81-2.52%). 
    The 3D line plot indicates diverse trends in liquid fuel consumption from 1991 to 2003, with India experiencing fluctuations,
    Canada showing stability, Germany consistently increasing, the UK fluctuating, and Switzerland decreasing with fluctuations. 
    The pie chart highlights the varied contributions of countries to gaseous fuel emissions in 2002, 
    and  The area plot illustrates the evolution of CO2 emissions from gaseous fuel consumption (1991-2003) for India, Canada, Germany, the United Kingdom, and Switzerland. 
    In India, there was a steady decrease from 3.88% in 1991 to 4.92% in 2003. """
    fig.text(0.5, 0.0, conclusion_text, ha='center', fontsize=14, va='center')

    fig.suptitle('CO2 Emissions Dashboard: Solid Fuel, Liquid Fuel, and Gaseous Fuel Consumption',
                 fontweight='bold', fontsize=20)
    plt.savefig("22078150", dpi=300)

    plt.show()


def main():
    # Use forward slashes for path consistency
    file_path = r"/Users/akarshaanjanan/Downloads/CO2_emissions.csv"
    data = read_data(file_path)
    indicator_to_plot = 'CO2 emissions from solid fuel consumption (% of total)'
    indicator_area_plot = 'CO2 emissions from gaseous fuel consumption (% of total)'
    line_plot_indicator = 'CO2 emissions from liquid fuel consumption (% of total)'
    countries_to_plot = ['India', 'Canada',
                         'Germany', 'United Kingdom', 'Switzerland']
    selected_years = [1991, 1993, 1995, 1997, 1999, 2003]
    start_year = 1991
    end_year = 2003

    # Use descriptive variable names
    plot_stacked_bar_visualization(
        data, indicator_to_plot, selected_years, countries_to_plot)
    plot_3d_linegraph(data, line_plot_indicator, start_year,
                      end_year, countries_to_plot)
    pie_chart_visualization(data, indicator_area_plot, 2002)

    area_plot_visualization(data, indicator_area_plot,
                            start_year, end_year, countries_to_plot)

    create_dashboard(data, countries_to_plot)


if __name__ == '__main__':
    main()
