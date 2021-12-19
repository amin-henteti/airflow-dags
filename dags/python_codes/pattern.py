import re
ch = """0
1
00:00:00,410 --> 00:00:03,530
Let us start our project by creating the input file folder.
2
00:00:03,530 --> 00:00:04,530

00:00:04,530 --> 00:00:13,209
I will give it name store_files.
3

4
00:00:13,209 --> 00:00:15,650
Daily our input file is going to land in this
directory.
4"""
print(re.findall(r'[\d:,>-]*?\n', ch))