/* Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
*/

package org.nasa.jpl.nexus.ingest.nexussink;

import com.amazonaws.services.s3.AmazonS3Client;
import com.amazonaws.services.s3.S3ClientOptions;
import org.apache.solr.client.solrj.SolrClient;
import org.apache.solr.client.solrj.embedded.EmbeddedSolrServer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.core.env.Environment;
import org.springframework.core.io.ClassPathResource;
import org.springframework.data.solr.core.SolrOperations;
import org.springframework.data.solr.core.SolrTemplate;

import javax.annotation.Resource;
import java.io.IOException;
import java.nio.file.Path;

/**
 * Created by greguska on 4/4/16.
 */
@Configuration
public class TestInfrastructureConfiguration {

    @Configuration
    @Profile("solr-embedded")
    static class SolrEmbeddedConfiguration {
        @Resource
        private Environment environment;

        @Value("#{environment[T(org.nasa.jpl.nexus.ingest.nexussink.NexusSinkOptionsMetadata).PROPERTY_NAME_SOLR_COLLECTION]}")
        private String solrCollection;

        @Value("#{environment[T(org.nasa.jpl.nexus.ingest.nexussink.NexusSinkOptionsMetadata).PROPERTY_NAME_SOLR_SERVER_URL]}")
        private String solrUrl;

        @Bean
        public SolrClient solrClient() throws IOException {
            Path solrHome = new ClassPathResource("solr").getFile().toPath();
            return new EmbeddedSolrServer(solrHome, solrCollection);
        }

        @Bean
        public SolrOperations solrTemplate(SolrClient solrClient) {
            return new SolrTemplate(solrClient);
        }

        @Bean
        public MetadataStore metadataStore(SolrOperations solrTemplate) {
            MetadataStore metadataStore = new SolrStore(solrTemplate);
            return metadataStore;
        }

    }

    @Configuration
    @Profile("s3local")
    static class S3LocalConfiguration {
        @Value("#{environment[T(org.nasa.jpl.nexus.ingest.nexussink.NexusSinkOptionsMetadata).PROPERTY_NAME_S3_BUCKET]}")
        private String s3BucketName;

        @Bean
        public AmazonS3Client s3client() {
            AmazonS3Client s3Client = new AmazonS3Client();
            S3ClientOptions s3ClientOptions = S3ClientOptions.builder().setPathStyleAccess(true).build();
            s3Client.setS3ClientOptions(s3ClientOptions);
            s3Client.setEndpoint("http://localhost:8080");
            return s3Client;
        }

        @Bean
        public DataStore dataStore(AmazonS3Client s3Client) {
            S3Store s3Store = new S3Store(s3Client, s3BucketName);
            return s3Store;
        }
    }

}