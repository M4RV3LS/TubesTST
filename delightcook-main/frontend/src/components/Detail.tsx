"use client";

import React, { useState } from 'react';
import { Text, Image, VStack, Heading, IconButton, HStack, Spacer, Switch } from '@chakra-ui/react';
import axios from 'axios';
import { Card } from './Card';
import Navbar from './Navbar';

export interface DetailProps {
    menu_items: {
        menu_id: number;
        menu_name: string;
        price: number;
        duration: number;
        calories: number;
        level: string;
        menu_url: string;
        description: string;
    }[],
    status: boolean
}

export default function Detail(props: any){
    const isLogin = (props.status == true);
    const isNotLogin = (props.status == false);
    return(
        <>
        { isLogin &&
        <Navbar status={true}/>
        }
        { isNotLogin &&
        <Navbar status={false}/>
        }
        <VStack h={'100%'} w={'100vw'} align={'left'}>
            {props.menu_items.map((data: any) => (
                <React.Fragment key={data.menu_id}>
                    <Image
                    style={{objectFit: 'cover'}}
                    alt='Katalog menu'
                    maxWidth={'100vw'}
                    maxHeight={'12vw'}
                    src={data.menu_url}/>
                    <Heading
                    fontWeight={"bold"}
                    fontSize={50}
                    color="#02033B"
                    whiteSpace={"nowrap"}
                    marginLeft="6%"
                    marginRight="6%"
                    mt={8}
                    >
                    {data.menu_name}
                    </Heading>
                    <HStack
                    mt={8}
                    maxW="full"
                    alignItems={'left'}
                    marginLeft="6%"
                    marginRight="6%"
                    >
                    <Text w={'70%'} whiteSpace="pre-line" mr={"6%"} textAlign={'justify'}>
                        {data.description}
                    </Text>
                    <Spacer></Spacer>
                    <HStack align={'top'} height={'100%'}>
                        { isLogin && 
                        <Card
                        key={data.menu_id}
                        menu_items={[data]}
                        status = {true}
                        detail = {true}/>
                        }
                        { isNotLogin && 
                        <Card
                        key={data.menu_id}
                        menu_items={[data]}
                        status = {false}
                        detail = {true}/>
                        }
                    </HStack>
                    </HStack>
                </React.Fragment>
            ))}
        </VStack>
        </>
    )
}