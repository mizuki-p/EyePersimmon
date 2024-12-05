function HistoryMessages({ messages }) {
  return (
    <div className="h-64 w-full bg-gray-900 text-white font-mono p-4 overflow-y-auto rounded-lg shadow-lg">
        <ul className="space-y-1">
            {messages.map((msg, index) => (
                <li key={index} className="whitespace-pre-wrap">
                {msg}
                </li>
            ))}
        </ul>
    </div>
  );
}

export default HistoryMessages;