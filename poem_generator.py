import torch
import torch.nn as nn
from transformers import GPT2Tokenizer, GPT2LMHeadModel

class GedichtenGenerator:

    def __init__(self,model_path,tokenizer_path):
        self.tokenizer = GPT2Tokenizer.from_pretrained(tokenizer_path)
        self.model = GPT2LMHeadModel.from_pretrained(model_path)

    def generate_word(self, tokens_tensor, temperature=1.0):
        """ 
        Sample a word given a tensor of tokens of previous words from a model. Given 
        the words we have, sample a plausible word. Temperature is used for 
        controlling randomness. If using temperature==0 we simply use a greedy arg max. 
        Else, we sample from a multinomial distribution using a lower inverse 
        temperature to allow for more randomness to escape repetitions. 
        """
        with torch.no_grad():
            outputs = self.model(tokens_tensor)
            predictions = outputs[0]
            if temperature>0:
                # Make the distribution more or less skewed based on the temperature
                predictions = outputs[0]/temperature
                # Sample from the distribution
                softmax = nn.Softmax(dim=0)
                predicted_index = torch.multinomial(softmax(predictions[0,-1,:]),1).item()
            else:
                # Simply take the arg-max of the distribution
                predicted_index = torch.argmax(predictions[0, -1, :]).item()
            # Decode the encoding to the corresponding word
            predicted_text = self.tokenizer.decode([predicted_index])
            return predicted_text

    def generate_sentence(self, initial_text, temperature=1.0):
        """ Generate a sentence given some initial text using a model and a tokenizer. Returns the new sentence. """
        self.model.eval()
    
        # Encode a text inputs
        text = ""
        sentence = text

        # We avoid an infinite loop by setting a maximum range
        for i in range(0,30):
            indexed_tokens = self.tokenizer.encode(initial_text + text)
      
            # Convert indexed tokens in a PyTorch tensor
            tokens_tensor = torch.tensor([indexed_tokens])
    
            new_word = self.generate_word(tokens_tensor, temperature=temperature)

            # Here the temperature is slowly decreased with each generated word,
            # this ensures that the sentence (ending) makes more sense.
            # We don't decrease to a temperature of 0.0 to leave some randomness in.
            if temperature<(1-0.008):
                temperature += 0.008
            else:
                temperature = 0.996

            text = text+new_word

            # Stop generating new words when we have reached the end of the line or the poem
            if "<|endoftext|>" in new_word:
                # returns new sentence and whether poem is done
                return (text.replace("<|endoftext|>","").strip(), True)
            elif '/' in new_word:
                return (text.strip(), False)
  
        return (text.strip(), True)

    def old_generate_word(self, tokens_tensor, temperature=1.0):
        with torch.no_grad():
            outputs = self.model(tokens_tensor)
            predictions = outputs[0]/temperature
            if temperature<1:
                softmax = nn.Softmax(dim=0)
                predicted_index = torch.multinomial(softmax(predictions[0,-1,:]),1).item()
            else:
                predicted_index = torch.argmax(predictions[0, -1, :]).item()
            predicted_text = self.tokenizer.decode([predicted_index])
        return predicted_text

    def old_generate_sentence(self, initial_text, temperature=1.0):
        self.model.eval()
        
        # Encode a text inputs
        text = ""
        sentence = text

        for i in range(0,30):
            indexed_tokens = self.tokenizer.encode(initial_text + text)
            
            # Convert indexed tokens in a PyTorch tensor
            tokens_tensor = torch.tensor([indexed_tokens])
            
            new_word = self.generate_word(tokens_tensor, temperature=temperature)

            if temperature<(1-0.008):
                temperature += 0.008
            else:
                temperature = 0.996

            text = text+new_word

            if "<|endoftext|>" in new_word:
                # returns new sentence and whether poem is done
                return (text.replace("<|endoftext|>","").strip(), True)
            elif '/' in new_word:
                return (text.strip(), False)
            
        return ("ERROR 404 *BLIEP* GEDICHT NIET GEVONDEN..", True)
