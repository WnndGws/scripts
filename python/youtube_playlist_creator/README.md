# YouTube Playlist Creator

<<<<<<< HEAD
## Introduction

### Purpose of the Document

This program automates the process of combining videos from multiple YouTube source playlists into a single target playlist. It performs the following tasks:

- Excludes Watched Videos
- Fetches and Aggregates Videos
- Sorts by Upload Date
- Adds to Target Playlist
- Authentication and API Interaction
- Caching

### Target Audience and Their Level of Technical Expertise

The target audience for this program is YouTube users who want to automate and streamline the management of their playlists, particularly those who:

- Follow Multiple Source Playlists:
  - Users who subscribe to several YouTube playlists and wish to aggregate new content into a single, personalized playlist.
- Avoid Duplicates and Watched Videos:
  - Individuals who want to ensure that their combined playlist contains only new, unwatched videos, avoiding any duplicates or previously viewed content.
- Prefer Chronologically Ordered Content:
  - Users who appreciate having videos sorted by their upload dates to watch content in the order it was released.

Required Level of Expertise:

- Intermediate Technical Proficiency:
  - Users should have a moderate understanding of Python programming. This includes the ability to install Python packages, run scripts from the command line, and modify configuration files.
  - Familiarity with APIs and OAuth 2.0:
  - Some knowledge of how APIs work, particularly the YouTube Data API, and the OAuth 2.0 authentication process is beneficial. Users will need to set up OAuth credentials and understand scopes and tokens.
  - Comfort with Command-Line Interfaces: Since the program uses typer for CLI interactions, users should be comfortable executing commands and scripts in a terminal or command prompt environment.

### Overview of the Code and Its Significance

## Installation and Setup

### System Requirements

### Prerequisites and Dependencies

### Step-by-Step Installation Instructions

### Configuration Options

## Getting Started

### High-Level Architecture Overview

### Main Features and Functionalities

### Basic Usage Examples

### Important Concepts and Terminology

## Code Structure

### Overview of the Directory/File Structure

### Description of Each Major Component/Module

### Interdependencies Between Different Parts of the Code

## API Documentation (if necessary)

### Overview of the Available APIs

### Detailed Explanation of Input Parameters and Expected Outputs

### Sample API Requests and Responses

## Configuration and Customization (if necessary)

### Explanation of Configuration Files or Settings

### How to Customize the Code for Specific Use Cases

### Best Practices and Recommended Configurations

## Troubleshooting and FAQs (if necessary)

### Common Issues and Their Solutions

### Error Messages and Their Meanings

### Frequently Asked Questions and Their Answers

## Performance Optimization (if necessary)

### Techniques for Improving Code Performance

## Security Considerations (if necessary)

### Potential Security Vulnerabilities and Their Mitigation
||||||| parent of 3b601b7 (first folder)
=======
---

## Introduction

### Purpose of the Document

This document provides details on using the YouTube Playlist Creator, a tool designed to combine videos from multiple YouTube playlists into a target playlist while filtering out watched videos and sorting them by upload date.

### Target Audience and Their Level of Technical Expertise

The target audience includes developers and system administrators familiar with Python, HTTP APIs, and basic OAuth 2.0 concepts.

### Overview of the Code and Its Significance

The tool uses OAuth 2.0 for YouTube API authentication, fetches video data from source playlists, filters out already-watched content, and sorts new content by upload date before adding it to the target playlist. It automates playlist management with minimal user intervention.

---

## Installation and Setup

### System Requirements

    Python 3.12 or higher
    Internet connection
    YouTube Data API access (OAuth credentials required)

### Prerequisites and Dependencies

Install the necessary Python libraries using the following command:

pip install httpx typer loguru pydantic rich

### Step-by-Step Installation Instructions

    Clone the repository.
    Ensure Python 3.12 is installed.
    Install dependencies using the command above.
    Place your OAuth credentials in yt_playlist_creator.ini.

### Configuration Options

Edit yt_playlist_creator.ini:

    client_id and client_secret: Your OAuth credentials.
    source_playlist_ids: Comma-separated YouTube playlist IDs to combine.
    target_playlist_id: The ID of the target playlist.
    watched_playlist_ids: List of playlist IDs marking videos as watched.

---

## Getting Started

### High-Level Architecture Overview

The tool consists of functions for:

    OAuth 2.0 authentication
    Fetching videos from playlists
    Filtering out watched content
    Adding videos to a target playlist

### Main Features and Functionalities

    Combines multiple source playlists.
    Filters out watched videos.
    Sorts videos by upload date.

### Basic Usage Examples

Run the tool using:

python youtube_playlist_creator.py combine_playlists

### Important Concepts and Terminology

    OAuth 2.0: Authentication protocol used for API access.
    YouTube API: API used for interacting with YouTube playlists.

---

## Code Structure

### Overview of the Directory/File Structure

    youtube_playlist_creator.py: Main script.
    yt_playlist_creator.ini: Configuration file.
    yt_playlist_creator.json: Token file for OAuth tokens.
    yt_playlist_cache.json: Caching file for video data.

### Description of Each Major Component/Module

    Config and Token Management: Handles loading and saving of configuration and OAuth tokens.
    YouTube API Interaction: Fetches and processes playlist data using the YouTube API.
    Main Application Command: Combines playlists as per user configuration.

### Interdependencies Between Different Parts of the Code

    OAuth and token functions depend on configuration data.
    Playlist processing relies on authenticated API calls.

---

## API Documentation (if necessary)

### Overview of the Available APIs

Uses YouTube Data API v3.

### Detailed Explanation of Input Parameters and Expected Outputs

    Input: Playlist IDs, OAuth credentials.
    Output: Updated target playlist.

### Sample API Requests and Responses

Sample API requests are constructed using httpx for interacting with YouTube's API.

---

## Configuration and Customization (if necessary)

### Explanation of Configuration Files or Settings

yt_playlist_creator.ini stores API credentials and playlist information.

### How to Customize the Code for Specific Use Cases

Modify source_playlist_ids and target_playlist_id in the configuration file.

### Best Practices and Recommended Configurations

## Ensure OAuth credentials are kept private

## Troubleshooting and FAQs (if necessary)

### Common Issues and Their Solutions

    Issue: Authentication failure.
        Solution: Check your OAuth credentials and permissions.

### Error Messages and Their Meanings

    Errors are logged in yt_playlist_creator.log.

### Frequently Asked Questions and Their Answers

    Q: Can I use more than one target playlist?
        A: Currently, only one target playlist is supported.

---

## Performance Optimization (if necessary)

### Techniques for Improving Code Performance

    Cached video data minimizes redundant API calls.

---

## Security Considerations (if necessary)

### Potential Security Vulnerabilities and Their Mitigation

OAuth tokens are saved locally; ensure the file is secure.
>>>>>>> 3b601b7 (first folder)
