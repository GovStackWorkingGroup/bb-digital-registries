// Script used in mockoon API assembly. Executed in docker-compose it merges all api files into single 
// file with common name. Should be executed from root

const path = require('path');
const yaml = require('js-yaml');
const YAML = require('yaml')
const fs = require('fs');

const directoryPath = path.join(__dirname, 'api');
const assemblyApiFileName = 'AssemblyApiDefinition.yaml'

function validateUnique(existingPaths, newPaths, propertyType) { 
    for (const property in newPaths) {
        if (property in existingPaths){
            console.warn(`Assembly's ${propertyType} ${property} already defined in assembly API. Definition will be overwritten.`);
        }
    }
}

function extendObjectProperty(existingObj, newObj, property) {
    validateUnique(existingObj[property], newObj[property], property)
    if (!!newObj[property]) {
        existingObj[property] = {...existingObj[property], ...newObj[property]}
    }
}

function saveApiDefinition(jsonApiDefinition) {
    const filePath = path.join(directoryPath, assemblyApiFileName)
    const doc = new YAML.Document();
    doc.contents = jsonApiDefinition;
    fs.writeFile(filePath, doc.toString(), function (err) {
        if (err) return console.error(err);
        console.log(`YAML definition saved as ${filePath}`);
    });
}

function loadApiYAMLs() {
    let fileArray = [] 
    let assembly =    {
        openapi: '3.0.0',
        info: {
          title: 'GovStack Digital registries BB Database API template',
          description: 'This is a sample API\n',
          version: '1.0.0',
          termsOfService: '#',
        },
        paths: {
        },
        components: {
            securitySchemes: {},
            parameters: {},
            schemas: {}
        }
      }

    // Paths and contexts from across multiple .yaml files 
    fs.readdir(directoryPath, function (err, files) {
        //handling error
        if (err) {
            return console.log('Unable to scan directory: ' + err);
        } 
        //listing all files using forEach
        files.forEach(function (file) {
            // Do whatever you want to do with the file
            if (file.endsWith('yaml')) {
                const apiDir = path.join(directoryPath, file)
                const nextYAML = yaml.load(fs.readFileSync(apiDir, 'utf8'))
                extendObjectProperty(assembly, nextYAML, 'paths')
                extendObjectProperty(assembly.components, nextYAML.components, 'schemas')
                extendObjectProperty(assembly.components, nextYAML.components, 'parameters')
                extendObjectProperty(assembly.components, nextYAML.components, 'securitySchemes')
            } else {
                console.warn("Found non YAML file in api directory. It'll not used in API definiion. [%s]", file)
            }
        });
        saveApiDefinition(assembly)
    });
}

loadApiYAMLs()
