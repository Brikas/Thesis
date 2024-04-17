from typing import List
import fb_msg_reader as fb
import re
import tiktoken
import shared_utils as utils




class PersonaEncoder:
    chats: dict
    selectedChats: dict

    def __init__(self):
        self.chats = {}
        self.selectedChats = {}

    def parse_fb_messages(self, filenames, name_id, limit = None) -> None:
        msgs = fb.get_messages_from_JSONs(filenames=filenames, limit=limit)
        self.chats[name_id] = msgs
        print(f"Messages saved to self.chats['{name_id}']")


    def filter_chats_empty(self):
        for nameid, chat in self.chats.items():
            filteredChat = []
            for msg in chat:
                if msg.content == "" or msg.content == None:
                    continue
                filteredChat.append(msg)
            self.chats[nameid] = filteredChat
            

    def filter_chats_regex(self, blacklist_re_patterns):
        # Instantiate filter log
        logs = {}
        for filter in blacklist_re_patterns:
            logs[filter["id"]] = 0

        for nameid, chat in self.chats.items():
            filteredChat = []
            for msg in chat:
                _excludeCurrent = False
                for filter in blacklist_re_patterns:
                    if bool(re.search(filter["pattern"] , msg.content)):
                        logs[filter["id"]] = logs[filter["id"]] + 1
                        _excludeCurrent = True
                        break
                if _excludeCurrent: continue
                filteredChat.append(msg)
            self.chats[nameid] = filteredChat

        print("Filtering")
        for key,value in logs.items():
            print(f"{key}: {value}")

    def _strinfigy_chat(chat: List[fb.Message]):
        blocks = []
        for msg in chat:
            block = f"{msg.sender}: {msg.content}"
            blocks.append(block)
        return "\n".join(blocks) 

    def select_chat_limited_by_tokens(self, nameid, token_count, start_msg = 0, speed = 1):
        chat = self.chats[nameid]
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

        finalChat = []
        for i, msg in enumerate(chat):
            if i % speed == 0:
                fullText = PersonaEncoder._strinfigy_chat(finalChat)
                num_tokens = len(encoding.encode(fullText))
                if num_tokens > token_count:
                    finalChat = finalChat[:-speed]
                    break
            finalChat.append(msg)
        
        finalTokens = final_tokens = len(encoding.encode(PersonaEncoder._strinfigy_chat(finalChat)))
        self.selectedChats[nameid] = finalChat
        print(f"Selected chat {nameid} for {final_tokens} ({len(finalChat)} messages)")

    def select_chat_full(self, nameid):
        finalChat = self.chats[nameid]
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        finalTokens = final_tokens = len(encoding.encode(PersonaEncoder._strinfigy_chat(finalChat)))
        self.selectedChats[nameid] = finalChat
        print(f"Selected chat {nameid} for {final_tokens} ({len(finalChat)} messages)")

    def count_chat_tokens(self, nameid):
        finalChat = self.chats[nameid]
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        finalTokens = final_tokens = len(encoding.encode(PersonaEncoder._strinfigy_chat(finalChat)))
        print(f"Chat {nameid} has {final_tokens} ({len(finalChat)} messages)")


    def count_all_selected_chat_tokens(self):
        chat_tokens = {}
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        for nameid, chat in self.selectedChats.items():
            tokens = len(encoding.encode(PersonaEncoder._strinfigy_chat(chat)))
            chat_tokens[nameid] = tokens
        return chat_tokens

    def output(self) -> str:
        finalText = ""
        for nameid, chat in self.selectedChats.items():
            finalText = finalText + PersonaEncoder._strinfigy_chat(chat)
        
        return finalText
    
