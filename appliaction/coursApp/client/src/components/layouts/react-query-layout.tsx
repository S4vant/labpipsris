import { QueryClientProvider, QueryClient } from "@tanstack/react-query";

const queryClient = new QueryClient();

function ReactQueryLayout() {
  return <QueryClientProvider client={queryClient}></QueryClientProvider>;
}

export default ReactQueryLayout;
