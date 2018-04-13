#! python3
# 
# Random Mixtape Maker - a computer program to generate randomized playlists
# from your music library. I saw something like this once on Donation Coder,
# but I can't find it anymore, and that one wasn't open source anyways. So I
# decided to make my own. 
#
# This program can only be run in the command line currently.
#
# Okay, I'm going to try and keep this simple. First big project in Python,
# first time using Github, lots of firsts for me in this. My formatting for
# the repo is probably going to be a little weird, and the style of programming
# may not be the best. Please bear with me on the next bit.

# Import os, argparse, random libraries
import os, argparse, random, pprint
from tinytag import TinyTag

# Create parser for command line arguments
parser = argparse.ArgumentParser(description='Finds songs in a directory and adds them to a random playlist.')
# Directory to search for sound files
parser.add_argument('directory',default='.\\', 
                    help='Path to top-level directory to search through for music')
# Name of playlist to create
parser.add_argument('playlist_name',default='playlist',
					help='Specifies the name of the created playlist')
# Includes sound file extensions to search for
parser.add_argument('file_extensions',default='mp3', nargs = '+',
					help='Specifies the file extensions that can be added to the playlist, single spaced')
# Sets limit for playlist length by duration
parser.add_argument('-time_length',type=int,
					help='Sets the maximum length of the playlist, in minutes')
# Sets limit for playlist length by song number
parser.add_argument('-track_nums',type=int,
					help='Sets the maximum number of tracks for the playlist')
# Recursive search setting
parser.add_argument('-query',default='q',choices = ['y','Y','n','N','q','Q'],
                    help='Determines if the program searches subfolders or not: Y - search subfolders | N - do not subfolders | Q - ask in program')
					
args = parser.parse_args()

# Main sound file search function
def song_search(folder, recursive, extensions):
	# Queries for search setting if not provided in arguments 
	if recursive == 'q':
		print('Would you like to search the subfolders included in this folder? [Y/N]')
		response = input('>> ')
		if response.lower() == 'y':
			recursive = 'y'
		if response.lower() == 'n':
			recursive = 'n'
			
	# Initializes list of songs
	song_list = []
	
	for extension in extensions:
		# Finds all <extension> files in the directory, adds to list
		if recursive == 'y':
			# Finds all <extension> files in directory, including subfolders
			for folder, subfolders, files in os.walk(folder):
				folder = os.path.abspath(folder)
				for file in files:
					if file.endswith(extension):
						song_list.append(os.path.join(folder,file))
		else:
			# Finds all <extension> files in directory, not including subfolders
			for file in os.listdir(folder):
				if file.endswith(extension):
					song_list.append(os.path.join(os.path.abspath(folder),file))
				
	# Return the song list
	return song_list

# Playlist creator function	
def playlist_maker(songs_list,track_num=None,max_duration=604800):
	while True:
		# Initialize variables
		random.shuffle(songs_list)
		playlist = songs_list
		name_list=[]
		duration = 0
		last_track = 0
		if track_num is None:
			track_num = 0
			
		# Limits playlist length based on duration
		for song in playlist:
			last_track += 1
			tag = TinyTag.get(song)
			duration += tag.duration
			if duration > max_duration:
				playlist = playlist[:last_track]
				
	
		# Limits playlist length based on number of tracks
		if track_num != 0:
			if track_num <= len(playlist):
				playlist = playlist[:track_num]
	
		# Displays list of song names to verify list for user	
		for song in playlist:
			name_list.append(os.path.basename(song))
		pprint.pprint(name_list)
		response = input('Is this playlist acceptable? [Y/N]')
	
		# Returns playlist if positive, redoes list if negative
		if response.lower() == 'y':
			return playlist
		else:
			continue

# Playlist writer function
def playlist_writer(playlist_name,playlist):
    # opens playlist file for writing
	playlist_file = open(playlist_name + '.m3u','w')
	# Writes songs in songs_list to playlist
	for song in playlist:
		playlist_file.write(song + '\n')
	playlist_file.close()
			
songs = song_search(args.directory,args.query,args.file_extensions)
playlist_made = playlist_maker(songs,args.track_nums,60*args.time_length)
playlist_writer(args.playlist_name,playlist_made)