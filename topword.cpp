#include <string>
#include <unordered_map>
#include <vector>
#include <algorithm>
#include <iostream>
#include <fstream>


// Organize arguments into a hashmap that is returned to be read later when opening files.
std::unordered_map<std::string, std::string> ParseArguments(std::string buffer) 
{
    std::unordered_map<std::string, std::string> argMap; 
    std::string field, value;


    for(int i = 0, j = buffer.length(), eq = 0, lastdelim = -1; i <= j; i ++)
    {
        if(buffer[i] == ';' || i == j) 
        {
            field = buffer.substr(lastdelim + 1, eq - lastdelim - 1);
            value = buffer.substr(eq + 1,  i - eq - 1);
            argMap[field] = value;

            lastdelim = i; 
            eq = 0;
        }
        else if(buffer[i] == '=') 
        {
            eq = i;
        } 

    }

    return argMap;
}

// Parse words with the specifications required and store then into a hash map and increment the frequency if they already exist.
std::unordered_map<std::string, int> ParseWords(std::ifstream& file) {
    std::unordered_map<std::string, int> tWords;
    std::string buffer = "";
    bool discardWord = false;
    char c;

    enum ReadingStates { READING_NONE, READING_LETTERS, READING_DIGITS} readingState = READING_NONE;

    while(file.get(c)) 
    {            
        if(discardWord) 
        {
            if(!isalnum(c)) // Continue until char other than num or alphabet
            { 
                discardWord = false;
                buffer = "";
                readingState = READING_NONE;
            }
            continue;
        }

        if(isdigit(c)) // Next char read is a digit (0-9)
        {
            if(readingState == READING_LETTERS) // Read digit while reading letters violation
            {
                discardWord = true;
                continue;
            } 
            else if(readingState == READING_NONE) {
                readingState = READING_DIGITS;
            }
        }
        else if(isalpha(c)) // Next char read is an alphabet (a-z,A-Z)
        {
            if(readingState == READING_DIGITS) // Read letter while reading numbers violation
            {
                discardWord = true;
                continue;
            } 
            else if(readingState == READING_NONE) {
                readingState = READING_LETTERS;
            }

            buffer += tolower(c);
        }
        else { // All other character handling.
            if(!buffer.empty() && buffer.length() <= 20) {
                ++tWords[buffer];
            }
            readingState = READING_NONE;
            buffer = "";
        }
    }

    // Check if buffer had something before termination.
    if(!buffer.empty() && buffer.length() <= 20) {
        ++tWords[buffer];
    }

    return tWords;
}

int main (int argc, char* argv[]) 
{
    /*
        Topword Program - COSC 4315
        Name: Muhaimin Badar
        User: cs07

        Implementation details:
            (1) Loops
            (2) Hash tables & vectors (dynamic arrays)
            (3) Should be able to handle inputs of arbitrary lengths as the program is implemented using dynamic containers.
                    -- Limited only by architecture and physical memory capacity.


    */

    if(argc != 2)
    {
        std::cout << "Invalid argument count." << std::endl;
        return EXIT_FAILURE;
    }

    // Parse arguments passsed.

    std::unordered_map<std::string, std::string> files = ParseArguments(argv[1]);

    if(!files.size()) {
        std::cout << "Invalid arguments provided.\nFormat: input=InputFileName;output=OutputFileName" << std::endl;
        return EXIT_FAILURE;
    }
    
    // Open input file and queue for parsing.
    std::ifstream inputStream(files["input"], std::ifstream::in);
    std::unordered_map<std::string, int> words = ParseWords(inputStream);

    // Create new array as maps cannot be easily sorted
    std::vector<std::pair<std::string, int>> sortedWords;


    // Push elements into the new vector and record the highest frequency.
    int highestFreq = 0;
    for(auto &i : words) {
        if(i.second > highestFreq)
            highestFreq = i.second;
            
        sortedWords.push_back(i);
    }

    // Sort words with std::algorithm using a lambda comparator that first checks the frequency and then the words itself
    std::sort(sortedWords.begin(), sortedWords.end(), [](const auto& lhs, const auto& rhs) { 
        return lhs.second != rhs.second ? lhs.second > rhs.second : lhs.first < rhs.first; 
    });

    // Open output file.
    std::ofstream outputStream(files["output"], std::ofstream::out);


    // Print words until a lower frequency word is encountered (ties will be printed according to the secondary word sort earlier)
    for(auto &w : sortedWords) {
        if(w.second < highestFreq)
            break;

        outputStream << w.first << " " << w.second << "\n";
    }
    // End of program
    return EXIT_SUCCESS;
}