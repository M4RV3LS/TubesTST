import React from 'react';
import {SimpleGrid, SimpleGridProps, ChakraProvider, extendTheme, Flex} from '@chakra-ui/react'

interface CardWrapperProps extends SimpleGridProps{
    
}

const CardWrapper: React.FC<CardWrapperProps> = (props) => {
    return(
        <ChakraProvider>
            <Flex alignContent={'center'} justifyContent={'center'}>
                <SimpleGrid 
                columns={props.columns} 
                spacing='35px'
                pr='5vh'
                w='auto'
                h='full'
                pb={4}
                pt={4} 
                mt={4}
                overflowX={'auto'}
                overflowY={'auto'} 
                whiteSpace='nowrap'
                >
                    {props.children}
                </SimpleGrid>
            </Flex>
        </ChakraProvider>
    );
}

export default CardWrapper;