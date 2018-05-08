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
parser.add_argument('-d',required=True,
                    help='Path to top-level directory to search through for music')
# Name of playlist to create
parser.add_argument('-playlist',required=True,
					help='Specifies the name of the created playlist')
# Includes sound file extensions to search for
parser.add_argument('-ext',default='mp3', nargs = '*',
					help='Specifies the file extensions that can be added to the playlist, single spaced')
# Sets limit for playlist length by filesize of songs
parser.add_argument('-file_size',type=int,default=2000000000000,
					help='Sets the maximum size of the playlist\'s audio files, in bytes')
# Sets limit for playlist length by duration
parser.add_argument('-time_length',type=int,default=604800,
					help='Sets the maximum length of the playlist, in minutes')
# Sets limit for playlist length by song number
parser.add_argument('-track_nums',type=int,default=0,
					help='Sets the maximum number of tracks for the playlist')
# Genre inclusion arguments
parser.add_argument('-genre_include',type=str, nargs='*',
					help='Determines which genres should be included in the playlist. If a genre you want to include contains whitespace in the name, put the genre in quotes.')
# Genre exclusion arguments
parser.add_argument('-genre_exclude',type=str, nargs='*',
					help='Determines which genres should not be included in the playlist. If a genre you want to exclude contains whitespace in the name, put the genre in quotes.')
# Artist inclusion arguments
parser.add_argument('-artist_include',type = str, nargs='*',
					help='Determines which artists should be included in the playlist. If an artist you want to include contains whitespace in the name, put the artist in quotes.')
# Artist exclusion arguments
parser.add_argument('-artist_exclude',type = str, nargs='*',
					help='Determines which artists should not be included in the playlist. If an artist you want to exclude contains whitespace in the name, put the artist in quotes.')
# Album inclusion arguments
parser.add_argument('-album_include',type = str, nargs='*',
					help='Determines which albums should be included in the playlist. If an album you want to include contains whitespace in the name, put the album in quotes.')
# Album exclusion arguments
parser.add_argument('-album_exclude',type = str, nargs='*',
					help='Determines which albums should not be included in the playlist. If an album you want to exclude contains whitespace in the name, put the album in quotes.')
# Album inclusion arguments
parser.add_argument('-title_include',type = str, nargs='*',
					help='Determines which titles or keywords should be included in the playlist. If a title or keyword you want to include contains whitespace in the name, put the title or keyword in quotes.')
# Album exclusion arguments
parser.add_argument('-title_exclude',type = str, nargs='*',
					help='Determines which titles or keywords should not be included in the playlist. If a title or keyword you want to exclude contains whitespace in the name, put the title or keyword in quotes.')					
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
def playlist_maker(songs_list,track_num,max_duration,max_filesize,genres_included,genres_blacklisted,artists_included,artists_blacklisted,albums_included,albums_blacklisted,titles_included,titles_blacklisted):
	while True:
		# Initialize variables
		random.shuffle(songs_list)
		playlist = songs_list
		name_list=[]
		duration = 0
		last_track = 0
		file_size = 0
		new_playlist = []
		
        # Removes songs not matching genre inclusion criteria
		if genres_included != None:
			for genre in genres_included:
				for song in playlist:
					tag = TinyTag.get(song)
					if genre in tag.genre:
						new_playlist.append(song)
			playlist = new_playlist
			new_playlist = []
			
		# Removes songs that are have blacklisted genres
		if genres_blacklisted != None:
			new_playlist = playlist.copy()
			for genre in genres_blacklisted:
				for song in playlist:
					tag = TinyTag.get(song)
					if genre in tag.genre:
						new_playlist.remove(song)
			playlist = new_playlist
			new_playlist = []
			
		# Removes songs not matching artist inclusion criteria
		if artists_included != None:
			for artist in artists_included:
				for song in playlist:
					tag = TinyTag.get(song)
					if artist in tag.artist:
						new_playlist.append(song)
			playlist = new_playlist
			new_playlist = []
			
		# Removes songs with blacklisted artists
		if artists_blacklisted != None:
			new_playlist = playlist.copy()
			for artist in artists_blacklisted:
				for song in playlist:
					tag = TinyTag.get(song)
					if artist in tag.artist:
						new_playlist.remove(song)
			playlist = new_playlist
			new_playlist = []
			
		# Removes songs not matching album inclusion criteria
		if albums_included != None:
			for album in albums_included:
				for song in playlist:
					tag = TinyTag.get(song)
					if album in tag.album:
						new_playlist.append(song)
			playlist = new_playlist
			new_playlist = []
			
		# Removes songs in blacklisted albums
		if albums_blacklisted != None:
			new_playlist = playlist.copy()
			for album in albums_blacklisted:
				for song in playlist:
					tag = TinyTag.get(song)
					if album in tag.album:
						new_playlist.remove(song)
			playlist = new_playlist
			new_playlist = []
			
		# Removes songs not matching title inclusion criteria
		if titles_included != None:
			for title in titles_included:
				for song in playlist:
					tag = TinyTag.get(song)
					if title in tag.title:
						new_playlist.append(song)
			playlist = new_playlist
			new_playlist = []
			
		# Removes songs in blacklisted title
		if titles_blacklisted != None:
			new_playlist = playlist.copy()
			for title in titles_blacklisted:
				for song in playlist:
					tag = TinyTag.get(song)
					if title in tag.title:
						new_playlist.remove(song)
			playlist = new_playlist
			new_playlist = []
			
		# Limits playlist length based on filesizes
		for song in playlist:
			last_track += 1
			tag = TinyTag.get(song)
			file_size += tag.filesize
			if file_size > max_filesize:
				playlist = playlist[:last_track]
				break

		last_track = 0

		# Limits playlist length based on duration
		for song in playlist:
			last_track += 1
			tag = TinyTag.get(song)
			duration += tag.duration
			if duration > max_duration:
				playlist = playlist[:last_track]
				break

		last_track = 0

		# Limits playlist length based on number of tracks
		if track_num != 0:
			if track_num <= len(playlist):
				playlist = playlist[:track_num]
				
		# Removes any songs that may have reoccured in the playlist
		playlist = list(set(playlist))
		random.shuffle(playlist)
		
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
	
songs = song_search(args.d,args.query,args.ext)
playlist_made = playlist_maker(songs,args.track_nums,60*args.time_length,args.file_size,args.genre_include,args.genre_exclude,args.artist_include,args.artist_exclude,args.album_include,args.album_exclude,args.title_include,args.title_exclude)
playlist_writer(args.playlist,playlist_made)
