import anthropic 



while response.stop_reason == "tool_use":
    #run tool 
    #append all messages to messages 
    #call API again