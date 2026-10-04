import discord
import discord.ext
from discord.ext.commands import Bot
import os
import sys
import time
import socket

class LaxativeEngine:
   def __init__(self):
      self.word_list = self.load_word_list()
      self.validate_word_list()
   
   def load_word_list(self):
      """
      Load word list from text file
      """
      with open("word_list.txt", "r") as file:
         content = file.read()
         raw_list = content.split()
         formatted_list = []
         for word in raw_list:
            formatted_list.append(word.upper())
      return formatted_list
   
   def validate_word_list(self):
      """
      Make sure all words in dict are valid
      """
      print(f"{len(self.word_list)} words in dictionary.")
      for word in self.word_list:
         if len(word) != 4:
            raise Exception(f"Bad word length: {word} is len {len(word)}")
   
   def get_distance_metric(self, word_a, word_b):
      """
      Calculate the distance between two words
      """
      dist = 0
      for i in range(0, 4):
         if word_a[i] != word_b[i]:
            dist += 1
      return dist
   
   def get_neighbors(self, word):
      """
      Get all words 1 word off from argument
      """
      neighbors = []
      word = word.upper()
      for prospect in self.word_list:
         if self.get_distance_metric(word, prospect) == 1:
            neighbors.append(prospect)
      return neighbors
   
   def get_reply_message(self, word):
      """
      Get a reply formatted for a Discord message
      """
      str = word.upper() + ": \n"
      neighbors = self.get_neighbors(word)
      for i in range(len(neighbors)):
         str = str + neighbors[i]
         if i < len(neighbors) - 1:
            str = str + ", "
      return str
      

if __name__ == "__main__":
   lax_eng = LaxativeEngine()