"use client"
import React, { useEffect, useState } from 'react';
import { ChakraProvider, Heading } from "@chakra-ui/react";
import Detail from "@/components/Detail";
import { DetailProps } from "@/components/Detail";
import axios from 'axios';

export default function MenuDetail(){
    return(
        <ChakraProvider>
            <Detail menu_items={"get menu from backend"} status={true} />
        </ChakraProvider>
    )
}