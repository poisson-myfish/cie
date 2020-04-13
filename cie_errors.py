def ErrorAndQuit(error_content):
    print('ERROR: ' + error_content)
    quit()

def DebugMessage(debug_message):
    print('DEBUG: ' + debug_message)

def InternalError(error_content):
    print('INTERNAL ERROR: ' + error_content + '. Please create an issue, if not existent, on GitHub poisson-myfish/cie including this error message.')
    quit()