#! python3
# 
# Random Mixtape Maker - a computer program to generate randomized playlists
# from your music library. I saw something like this once on Donation Coder,
# but I can't find it anymore, and that one wasn't open source anyways. So I
# decided to make my own.
#
# Okay, I'm going to try and keep this simple. First big project in Python,
# first time using Github, lots of firsts for me in this. My formatting for
# the repo is probably going to be a little weird, and the style of programming
# may not be the best. Please bear with me on the next bit.

# Import os, argparse, random libraries
import os, argparse, random

# Create parser for command line arguments
parser = argparse.ArgumentParser(description='Finds songs in a directory and adds them to a random playlist.')
parser.add_argument('directory',default='.\\', 
					help='Path to top-level directory to search through for music')
parser.add_argument('playlist_name',default='playlist', 
					help='Specifies the name of the created playlist')
parser.add_argument('-query',default='q',choices = ['y','Y','n','N','q','Q'],
					help='Determines if the program searches subfolders or not: Y - search subfolders | N - do not subfolders | Q - ask in program')
					
args = parser.parse_args()

# Main mp3 sound file search function
def mp3_search(folder, recursive):
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
	
	# Finds all mp3 files in the directory, adds to list
	if recursive == 'y':
		# Finds all mp3s in directory, including subfolders
		for folder, subfolders, files in os.walk(folder):
			folder = os.path.abspath(folder)
			for file in files:
				if file.endswith('.mp3'):
					song_list.append(os.path.join(folder,file))
	else:
		# Finds all mp3s in directory, not including subfolders
		for file in os.listdir(folder):
			if file.endswith('.mp3'):
				song_list.append(os.path.join(os.path.abspath(folder),file))
				
	# Shuffle the song list
	random.shuffle(song_list)
	return song_list

# Playlist file writer function	
def playlist_maker(songs_list,playlist_name):
	# opens playlist file for writing
	playlist = open(playlist_name + '.m3u','w')
	# Writes all songs in songs_list to playlist
	for song in songs_list:
		playlist.write(song + '\n')
			
songs = mp3_search(args.directory,args.query)
print(songs)
playlist_maker(songs,args.playlist_name)

