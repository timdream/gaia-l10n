#!/usr/bin/python
""" Copyright (c) 2012 Fabien Cazenave, Mozilla.
  "
  " Permission is hereby granted, free of charge, to any person obtaining a copy
  " of this software and associated documentation files (the "Software"), to
  " deal in the Software without restriction, including without limitation the
  " rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
  " sell copies of the Software, and to permit persons to whom the Software is
  " furnished to do so, subject to the following conditions:
  "
  " The above copyright notice and this permission notice shall be included in
  " all copies or substantial portions of the Software.
  "
  " THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  " IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  " FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  " AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  " LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
  " FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
  " IN THE SOFTWARE.
  """

# Warning: I suck at writing Python, and this code has be done rather quickly.
import json
import os
import shutil
import sys

# Glogal variables! Hard-coded params!
# That's how you know this is such a great script. :-)
gSupportedLocales = ['ar', 'en-US', 'fr', 'ru', 'zh-TW']
gDefaultLocale = 'en-US'

# The expected file structure is as follows:
# /
#     [lang]/
#         [app]/
#             manifest.json
#             locale/
#                 [*].properties
#     ...

# inject localized name/descriptions into JSON manifests
def mergeManifests(inputDir, outputDir, application):
  manifestPath = os.path.join(outputDir, application, 'manifest.json')
  print(manifestPath)

  # load JSON manifest
  dest = open(manifestPath, 'r')
  data = json.load(dest)
  data['locales'] = {}
  data['default_locale'] = gDefaultLocale
  dest.close()

  # fill the 'locales' property
  for lang in gSupportedLocales:
    sourcePath = os.path.join(inputDir, lang, application, 'manifest.properties')
    source = open(sourcePath, 'r');

    # parse name/description in the properties file -- FIXME:
    # we expect to find 'name' on the first line, 'description' on the 2nd
    desc = {}
    lines = source.readlines()
    desc['name'] = lines[0].replace('name=', '').replace('\n', '')
    desc['description'] = lines[1].replace('description=', '').replace('\n', '')
    data['locales'][lang] = desc

    dest = open(manifestPath, 'wb')
    dest.write(json.dumps(data, indent = 2, separators=(',', ': ')))
    dest.close()

# concatenate files in the 'locale' directory (if any)
def mergeProperties(inputDir, outputDir, application):
  localeDir = os.path.join(inputDir, gDefaultLocale, application, 'locale')
  if os.path.isdir(localeDir):
    for resource in os.listdir(localeDir):

      resourcePath = os.path.join(outputDir, application, 'locale', resource)
      print(resourcePath)

      dest = open(resourcePath, 'wb')
      for lang in gSupportedLocales:
        dest.write('[' + lang + ']\n')
        sourcePath = os.path.join(inputDir, lang, application, 'locale', resource)
        shutil.copyfileobj(open(sourcePath, 'rb'), dest)

# import l10n data for all Gaia apps
def main():
  if not len(sys.argv) == 2:
    print('Usage: ' + sys.argv[0] + ' [applicationDirectory]')
    exit()

  inputDir = os.path.realpath(os.path.dirname(sys.argv[0]))
  outputDir = os.path.realpath(sys.argv[1])
  print('Importing manifests and properties...')
  print('  from: ' + inputDir)
  print('  into: ' + outputDir)

  appDir = os.path.join(inputDir, gDefaultLocale)
  for application in os.listdir(appDir):
    mergeManifests(inputDir, outputDir, application)
    mergeProperties(inputDir, outputDir, application)

# startup
if __name__ == "__main__":
  main()

