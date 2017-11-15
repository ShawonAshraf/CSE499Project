//
//  ViewController.swift
//  macOS_GUI
//
//  Created by Shawon Ashraf on 7/8/17.
//  Copyright © 2017 Shawon Ashraf. All rights reserved.
//

import Cocoa

class ViewController: NSViewController {

    @IBOutlet var imageView: NSImageView!
    @IBOutlet var loadImageButton: NSButton!
    @IBOutlet var recognizeButton: NSButton!
    @IBOutlet var resultLabel: NSTextField!
    
    
    var imagePath: String!
    var labelPath: String!
    var graphPath: String!
    
    let scriptPath = "/Users/shawon/Codes/ClassCodes/CSE499Project/gui_linker.py"
    
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }

    override var representedObject: Any? {
        didSet {
        // Update the view, if already loaded.
        }
    }
    
    
    @IBAction func loadImage(_ sender: Any) {
        // create the file open dialog
        
        let fileOpenDialog = NSOpenPanel()
        
        fileOpenDialog.title = "Select the image file"
        fileOpenDialog.showsResizeIndicator = true
        fileOpenDialog.canChooseFiles = true
        fileOpenDialog.canChooseDirectories = true
        fileOpenDialog.canCreateDirectories = true
        fileOpenDialog.allowsMultipleSelection = false
        fileOpenDialog.allowedFileTypes = ["png", "jpg", "jpeg"]
        
        // now call the dialog
        
        if (fileOpenDialog.runModal() == NSModalResponseOK) {
            let result = fileOpenDialog.url
            
            if (result != nil) {
                imagePath = result!.path
                
                // set image to image viewer
                let image = NSImage(byReferencingFile: imagePath!)
                imageView.image = image
            }
        }
        
    }

    
    @IBAction func recognizeFromImage(_ sender: Any) {
        // set label and graph path
        
        labelPath = "/Users/shawon/Codes/ClassCodes/CSE499Project/Classifier/Training/retrained_labels.txt"
        graphPath = "/Users/shawon/Codes/ClassCodes/CSE499Project/Classifier/Training/retrained_graph.pb"
        
        
        // initiate task for running script
        
        let task = Process()
        
        task.launchPath = "/Users/shawon/anaconda/envs/cse499/bin/python"
        task.arguments = [scriptPath, imagePath!, labelPath!, graphPath!]
        
        // create the pipe
        
        let pipe = Pipe()
        task.standardOutput = pipe
        
        // launch task
        task.launch()
        
        let data = pipe.fileHandleForReading.readDataToEndOfFile()
        let output = NSString(data: data, encoding: String.Encoding.utf8.rawValue)
        
        resultLabel.stringValue = output! as String
    }
    

}

