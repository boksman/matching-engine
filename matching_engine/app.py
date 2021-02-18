import fileinput
from typing import Iterator, Callable
from matching_engine.common.engine import MatchingEngine, MatchingEngineDefault
from matching_engine.common.helpers import print_stderr
from matching_engine.common.message_parser import MessageParserDefault, MessageParser


def main(input_iterator_func: Callable[[], Iterator[str]] = None,
         engine: MatchingEngine = None,
         parser: MessageParser = None):
    """
    Parse raw messages from input_iterator_func and pass to engine
    :param input_iterator_func: The source of raw data
    :param engine: Matching engine implementation
    :param parser: Parser to use
    :return:
    """

    input_iterator_func = input_iterator_func or fileinput.input
    engine = engine or MatchingEngineDefault()
    parser = parser or MessageParserDefault()

    for line in input_iterator_func():
        line = line.strip()
        mess = parser.parse(line)
        if mess is None:
            print_stderr(f"Malformed or unhandled input '{line}'")
            continue
        engine.process(mess)


if __name__ == "__main__":
    main()
