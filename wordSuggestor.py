class WordSuggestor:
    def __init__(self):
        self.word_freq = {}
        self.prefix_freq = {}

    def train(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            words = text.split()
            for word in words:
                word_lower = word.lower()  # Convert word to lowercase
                if word_lower in self.word_freq:
                    self.word_freq[word_lower] += 1
                else:
                    self.word_freq[word_lower] = 1

                # Update prefix frequency
                for i in range(1, len(word_lower)):
                    prefix = word_lower[:i]
                    if prefix in self.prefix_freq:
                        self.prefix_freq[prefix] += 1
                    else:
                        self.prefix_freq[prefix] = 1

    def suggest_words(self, prefix):
        prefix_lower = prefix.lower()  # Convert prefix to lowercase
        suggestions = []

        # Get prefixes with highest usage count
        top_prefixes = sorted(self.prefix_freq.keys(), key=lambda x: (-self.prefix_freq[x], len(x)))

        for p in top_prefixes:
            if p.startswith(prefix_lower):
                suggestions.append(p)

        # Return only the top 5 suggestions
        return suggestions[:5]
