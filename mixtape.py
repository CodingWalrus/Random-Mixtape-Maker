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
import os, argparse, random

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
			# Finds all mp3s in directory, including subfolders
			for folder, subfolders, files in os.walk(folder):
				folder = os.path.abspath(folder)
				for file in files:
					if file.endswith(extension):
						song_list.append(os.path.join(folder,file))
		else:
			# Finds all mp3s in directory, not including subfolders
			for file in os.listdir(folder):
				if file.endswith(extension):
					song_list.append(os.path.join(os.path.abspath(folder),file))
				
	# Shuffle the song list
	random.shuffle(song_list)
	return song_list

# Playlist file writer function	
def playlist_maker(songs_list,playlist_name,track_num=0):
	if track_num == 0:
		track_num = len(songs_list)
	# opens playlist file for writing
	playlist = open(playlist_name + '.m3u','w')
	# Writes songs in songs_list to playlist
	for i in range(track_num):
		playlist.write(songs_list[i] + '\n')
	playlist.close()
			
songs = song_search(args.directory,args.query,args.file_extensions)
playlist_maker(songs,args.playlist_name,args.track_nums)

