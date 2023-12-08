import { ChakraProvider, Heading } from "@chakra-ui/react";
import Navbar from "@/components/Navbar";

export default function Menu(){
    return(
        <ChakraProvider>
            <Navbar />
            <Heading>
                Menu
            </Heading>
        </ChakraProvider>
    )
}