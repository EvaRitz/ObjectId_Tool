# ObjectId Tool

ObjectId Tool is a Maya tool that automatically assigns unique ObjectId 
float attributes to mesh shapes in bulk. It is designed to work alongside 
Houdini instancing pipelines, where ObjectId values on points determine 
which asset gets instanced at each location.

## Maya Version
ObjectId Tool was designed on Maya 2024 and supports Maya 2025+.

## Installation
Copy the contents of ObjectId_Tool.py into Maya's Script Editor.
You can drag and drop the selected code into any shelf to save it as a button.

## How to use
* Select one or more assets or groups in the outliner
* Input the starting ObjectId value
* Click "Add ObjectId to Shapes". the value increments automatically for each asset in a group

If ObjectId attributes already exist, the tool will ask for confirmation 
before overwriting.

## License
ObjectId Tool is available under the MIT License. You can use it for 
commercial or non-commercial projects. Be sure to credit me in the 
project and documentation.

## Project status
- Separate project into multiple files for clarity