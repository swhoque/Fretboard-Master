from statsdb_functions import *
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

def show_note_stats(master, conn, user_id):
    try:
        # Get stats using get_note_stats
        stats = get_note_stats(conn, user_id)
        
        # Create a figure and axes
        fig = Figure(figsize=(5, 4), dpi=100, facecolor='xkcd:brown', edgecolor='white')
        ax = fig.add_subplot(111)
        
        # Sample data for the bar chart
        categories = ["Notes Mastered", "Total Notes Hit", "Total Notes Missed"]
        values = [stat for stat in stats][1:]
        
        # Create the bar chart
        ax.bar(categories, values)
        
        # Embed the matplotlib figure into CustomTkinter using FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.draw()  # Draw the canvas
        
        # Pack the canvas widget into the app
        canvas.get_tk_widget().pack()
    except TypeError as e:
        print(f"Error showing stats: {e}")

def show_chord_stats(master, conn, user_id):
    try:
        # Get stats using get_chord_stats
        stats = get_chord_stats(conn, user_id)
        
        # Create a figure and axes
        fig = Figure(figsize=(5, 4), dpi=100, facecolor='xkcd:brown', edgecolor='white')
        ax = fig.add_subplot(111)
        
        # Sample data for the bar chart
        categories = ["Chords Mastered", "Total Chords Hit", "Total Chords Missed"]
        values = [stat for stat in stats][1:]
        
        # Create the bar chart
        ax.bar(categories, values)
        
        # Embed the matplotlib figure into CustomTkinter using FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.draw()  # Draw the canvas
        
        # Pack the canvas widget into the app
        canvas.get_tk_widget().pack()
    except TypeError as e:
        print(f"Error showing stats: {e}")


def show_scale_stats(master, conn, user_id):
    try:
        # Get stats using get_chord_stats
        stats = get_chord_stats(conn, user_id)
        
        # Create a figure and axes
        fig = Figure(figsize=(5, 4), dpi=100, facecolor='xkcd:brown', edgecolor='white')
        ax = fig.add_subplot(111)
        
        # Sample data for the bar chart
        categories = ["Scales Mastered", "Total Scales Hit", "Total Scales Missed"]
        values = [stat for stat in stats][1:]
        
        # Create the bar chart
        ax.bar(categories, values)
        
        # Embed the matplotlib figure into CustomTkinter using FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.draw()  # Draw the canvas
        
        # Pack the canvas widget into the app
        canvas.get_tk_widget().pack()
    except TypeError as e:
        print(f"Error showing stats: {e}")